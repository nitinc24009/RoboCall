import glob
import threading
import os

from modules import wav_clipper


def clip_wav(input_dir="./", output_dir="./", start_sec=0, end_sec=1, thread=10):
    """Read the files from the input directory and clips it from starting to end point and export to the output directory"""

    try:
        os.makedirs(output_dir, exist_ok=True)

        wav_files = os.listdir(input_dir)

        _thread_pool = []
        for file_count in range(len(wav_files)):
            fname = wav_files[file_count]
            if fname.endswith(".wav"):
                _thread = threading.Thread(target=wav_clipper.clip_wav_audio, args=(fname, input_dir, output_dir, start_sec, end_sec, ))
                _thread.start()

                _thread_pool.append(_thread)
                if len(_thread_pool)==thread or (file_count + 1)==len(wav_files):
                    for _thread in _thread_pool:
                        _thread.join()

                    _thread_pool = []

    except Exception as e:
        print(f"Error: {e}")


if __name__=="__main__":
    
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input",
        default="./",
        help="Input Directory"
    )
    parser.add_argument(
        "-o", "--output",
        default="./",
        help="Output Directory"
    )
    parser.add_argument(
        "-s", "--start",
        type=float,
        default=0,
        help="Start Time in Second"
    )
    parser.add_argument(
        "-e", "--end",
        type=float,
        default=1,
        help="End Time in Second"
    )
    parser.add_argument(
        "-t", "--thread",
        type=int,
        default=1,
        help="No. of Threads"
    )
    args = parser.parse_args()

    input_dir = args.input
    output_dir = args.output
    start_time = args.start
    end_time = args.end
    thread = args.thread

    clip_wav(input_dir=input_dir, output_dir=output_dir, start_sec=start_time, end_sec=end_time, thread=thread)

