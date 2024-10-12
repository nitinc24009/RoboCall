import os
import re
import requests
from bs4 import BeautifulSoup
from getpass import getpass
import time


def generate_auth_cookie(email=None, password=None):
    """Generate a cookie and authenticate it"""
    
    print(f"[*] Downloading Data From: https://sla2.talkbank.org/")
    login_url = "https://sla2.talkbank.org/logInUser"
    cookie = requests.get(login_url).headers["Set-Cookie"].split(";")[0]

    if email and password:
        creds = {
            "email": email,
            "pswd": password
        }
    elif email and not password:
        creds = {
            "email": email,
            "pswd": getpass("Enter Password: ")
        }
    else:
        print("[*] Credentials required for Human Call download. Please Login with your credentials.")
        creds = {
            "email": input("Enter Email: "),
            "pswd": getpass("Enter Password: ")
        }

    headers = {
        "Cookie": cookie,
    }
    r = requests.post(login_url, headers=headers, json=creds)

    return cookie


def download_humancall(download_dir, local_dir="data/", email=None, password=None):
    """Extracts the audio download URL and download the files"""

    download_dir = "HumanCall_Audio"
    download_dir = os.path.join(local_dir, download_dir)
    os.makedirs(download_dir, exist_ok=True)
    
    data_url = "https://media.talkbank.org/fileListing?bp=media&path=ca/CallHome/eng/0wav"
    headers = {"Cookie": generate_auth_cookie(email=email, password=password)}

    r = requests.get(
        data_url,
        headers=headers
    )

    if r.status_code==200:
        print("[*] Downloading Dataset ...")

    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all('a')

    for link in links:
        href = link.get('href')
        if "type=save" in href:
            ofname = re.findall(".*.wav", href.split("/")[-1])[0]

            if ofname not in os.listdir(download_dir):
                print(f"[*] Downloading: {ofname}", end="\r")

                try:
                    r = requests.get(href, headers=headers)
                except:
                    print("[!] Server Not Responding ... Retrying ... ")
                    time.sleep(5)
                    r = requests.get(href, headers=headers)
                audio_data = r.content

                if r.content:
                    file_name = f"{download_dir}/{ofname}"

                    with open(file_name, "wb") as f:
                        f.write(audio_data)
            
                    print(f"[+] Downloaded: {file_name}")

                else:
                    print(f"[-] Cannot Download: {file_name}")

    print("[+] Download Completed!")
    print(f"[+] Dataset Saved to: {download_dir}")

    return True


if __name__=="__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-e", "--email",
        help="Enter Email Manually",
        required=True
    )
    parser.add_argument(
        "-o", "--output",
        default="./",
        help="Output Directory"
    )
    args = parser.parse_args()

    email = args.email
    outdir = args.output

    download_audio(email=email, download_dir=outdir)

