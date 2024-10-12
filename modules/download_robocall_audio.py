import git
import os
import shutil

def download_subfolder_from_git(repo_url, subfolder_path, local_dir, temp_repo="__git_temp__"):
    """Downloads all the files from a particular directory of a GitHub Repository"""

    try:
        print(f"Downloading Data From: {repo_url}")
        git.Repo.clone_from(repo_url, temp_repo)  # Clone the repository into a temporary directory
        subfolder_full_path = os.path.join(temp_repo, subfolder_path)  # Copy the subfolder to the desired local directory
        shutil.copytree(subfolder_full_path, local_dir) # copy all the files from the cloned repo to the local directtory
        
        shutil.rmtree(temp_repo)      # Clean up the temporary cloned repository

        return True

    except:
        return False


def download_robocall(local_dir="./data/"):
    """Download RoboCall Dataset from the GitHub"""
    
    repo_url = "https://github.com/wspr-ncsu/robocall-audio-dataset"
    subfolder = "audio-wav-16khz"
    download_dir = "RoboCall_Audios"

    local_dir = os.path.join(local_dir, download_dir)

    res = download_subfolder_from_git(repo_url=repo_url, subfolder_path=subfolder, local_dir=local_dir)
    if res:
        print("[+] Download Completed!")
        print(f"[+] Dataset Saved to: {local_dir}")
    else:
        print("[-] Download Failed!")


