from matplotlib import pyplot as plt
import librosa
import numpy as np
import librosa.display
import os
import multiprocessing


class GenerateSpectrogram:

    def __init__(self, input_dir, output_dir, stype, multiprocess=50):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.multiprocess = multiprocess
        self.stype = stype


    def stft_spectrogram(self, audio_file):
        """
        Takes input the audio filename and generates STFT based spectrogram

        :param audio_file:
        :returns plt:
        :return img_name:
        """

        if audio_file.endswith("wav"):
            img_name = audio_file.split("/")[-1].replace(".wav", "_stft.png")

            y, sr = librosa.load(audio_file)
            y = librosa.resample(y, orig_sr=sr, target_sr=16000)
            X = librosa.stft(y=y)
            Xdb = librosa.amplitude_to_db(abs(X))

            librosa.display.specshow(Xdb, sr=sr, cmap='coolwarm', fmax=8000)
            plt.tight_layout()

            return plt, img_name

        else:
            return None, None


    def mel_spectrogram(self, audio_file):
        """
        Takes input the audio filename and generates Mel-spectrogram.

        :param audio_file: Path to the audio file
        :returns plt: Matplotlib plot object
        :return img_name: The name of the saved Mel-spectrogram image
        """

        if audio_file.endswith("wav"):
            img_name = audio_file.split("/")[-1].replace(".wav", "_mel.png")

            y, sr = librosa.load(audio_file)
            y = librosa.resample(y, orig_sr=sr, target_sr=16000)

            S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
            S_db = librosa.amplitude_to_db(S, ref=np.max)

            librosa.display.specshow(S_db, sr=sr, cmap='coolwarm', fmax=8000)
            plt.tight_layout()

            return plt, img_name

        else:
            return None, None



    def chroma_stft_spectrogram(self, audio_file):
        """
        Takes input the audio filename and generates STFT based spectrogram

        :param audio_file:
        :returns plt:
        :return img_name:
        """

        if audio_file.endswith("wav"):
            img_name = audio_file.split("/")[-1].replace(".wav", "_chroma_stft.png")

            y, sr = librosa.load(audio_file)
            y = librosa.resample(y, orig_sr=sr, target_sr=16000)
            X = np.abs(librosa.stft(y))
            Xdb = librosa.feature.chroma_stft(S=X, sr=sr)

            librosa.display.specshow(Xdb, sr=sr, cmap='coolwarm')

            lower_limit = 0
            upper_limit = 5000
            plt.ylim(lower_limit, upper_limit)

            plt.tight_layout()

            return plt, img_name

        else:
            return None, None


    def chroma_cqt_spectrogram(self, audio_file):
        """
        Takes input the audio filename and generates STFT based spectrogram

        :param audio_file:
        :returns plt:
        :return img_name:
        """

        if audio_file.endswith("wav"):
            img_name = audio_file.split("/")[-1].replace(".wav", "_chroma_cqt.png")

            y, sr = librosa.load(audio_file)
            Xdb = librosa.feature.chroma_cqt(y=y, sr=sr)

            librosa.display.specshow(Xdb, sr=sr, cmap='coolwarm', x_axis='time', y_axis='hz')

            plt.tight_layout()

            return plt, img_name

        else:
            return None, None


    def save_spectrogram(self, audio_file):
        """
        Generate spectrogram image from audio file

        :param audio_file:
        :return:
        """

        plot, img_name = None, None

        if self.stype=="stft_spectrogram":
            plot, img_name = self.stft_spectrogram(audio_file=audio_file)

        if self.stype=="chroma_stft_spectrogram":
            plot, img_name = self.chroma_stft_spectrogram(audio_file=audio_file)

        if self.stype=="chroma_cqt_spectrogram":
            plot, img_name = self.chroma_cqt_spectrogram(audio_file=audio_file)

        if self.stype=="mel_spectrogram":
            plot, img_name = self.mel_spectrogram(audio_file=audio_file)

        # Save Spectrogram
        if plot and img_name:
            ofname = f"{self.output_dir}/{img_name}"
            plot.savefig(ofname)


    def store_spectrogram(self):
        """
        Read the audio files from the input directory, generates spectrograms
        and save in the output directory

        :return None:
        """

        # create output directory if not present
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

        # conversion
        if os.path.isdir(self.input_dir):
            process_pool = []
            process_count = 0

            for audio_filename in os.listdir(self.input_dir):
                audio_filename = f"{self.input_dir}/{audio_filename}"
                if os.path.isfile(audio_filename):
                    if audio_filename.endswith("wav"):

                        process = multiprocessing.Process(target=self.save_spectrogram, args=(audio_filename,))

                        process_pool.append(process)
                        process.start()
                        process_count += 1

                        if (process_count%self.multiprocess==0 or len(os.listdir(self.input_dir))==process_count):
                            for _process in process_pool:
                                _process.join()
