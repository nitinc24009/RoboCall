import argparse

from modules import spectrogram


def main(input_dir, stype, output_dir, processes):

    options_dict = {
        "stft": "stft_spectrogram",
        "chroma_stft": "chroma_stft_spectrogram",
        "chroma_cqt": "chroma_cqt_spectrogram",
        "mel": "mel_spectrogram"
    }

    spec = spectrogram.GenerateSpectrogram(input_dir=input_dir, output_dir=output_dir, multiprocess=processes, stype=options_dict[stype])
    spec.store_spectrogram()



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", help="Directory where the Audio Files are Stored",
    )
    parser.add_argument(
        "-s", "--spectrogram", choices=["stft", "chroma_stft", "chroma_cqt"], help="Set Spectrogram Type",
    )
    parser.add_argument(
        "-o", "--output", help="Directory where to Store the Converted Audio Files"
    )
    parser.add_argument(
        "-p", "--process", type=int, default=1, help="Number of Parallel Processes"
    )
    args = parser.parse_args()

    input_dir = args.input
    stype = args.spectrogram
    output_dir = args.output
    processes = args.process

    main(input_dir=input_dir, stype=stype, output_dir=output_dir, processes=processes)