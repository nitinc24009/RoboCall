from modules import download_humancall_audio as dhc
from modules import download_robocall_audio as drc
import argparse


def download_human_audio(download_local_dir = "./data"):
    dhc.download_humancall(local_dir=download_local_dir)


def download_robocall_audio(download_local_dir = "./data"):
    drc.download_robocall(local_dir=download_local_dir)


def download(output_local_path="./data", flag="ALL"):
    if flag == "ALL":
        download_robocall_audio(download_local_dir=output_local_path)
        download_human_audio(download_local_dir=output_local_path)

    elif flag == "HUMAN":
        download_human_audio()

    elif flag == "ROBO":
        download_robocall_audio()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--output",
        default="./",
        help="Output Directory"
    )
    parser.add_argument(
        "-f", "--flag",
        default="ALL",
        choices=["ALL", "HUMAN", "ROBO"],
        help="Download FLAG {ALL, HUMAN, ROBO}"
    )
    args = parser.parse_args()

    outdir = args.output
    flag = args.flag.upper()
    
    download(output_local_path=outdir, flag=flag)

