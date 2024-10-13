import librosa
import soundfile as sf


def clip_wav_audio(fname, input_dir, outdir, start_sec, end_sec, sr=16000):
    """Clips a WAV audio file based on starting and ending seconds."""
  
    try:
        audio_file = f"{input_dir}/{fname}"
        y, sr = librosa.load(audio_file, sr=sr)
        # print(f">> Fs: {sr}")

        start_sample = int(start_sec * sr)
        end_sample = int(end_sec * sr)

        clipped_audio = y[start_sample:end_sample]

        output_file = f"{outdir}/{fname.replace('.wav', '_clipped.wav')}"
        sf.write(output_file, clipped_audio, sr)

    except Exception as e:
        print(f"Error clipping audio: {e}")