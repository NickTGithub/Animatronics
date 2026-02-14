import librosa
import scipy.io.wavfile as wavfile
import numpy as np

def downsample_audio(input_file, output_file, target_sample_rate):
    """
    Downsamples an audio file to a target sample rate using librosa.

    Args:
        input_file (str): Path to the input audio file.
        output_file (str): Path to save the downsampled audio file.
        target_sample_rate (int): The desired new sample rate (e.g., 16000 Hz).
    """
    try:
        # Load the audio file and resample simultaneously
        # librosa.load performs high-quality resampling and returns 
        # the audio time series (y) and the original sample rate (orig_sr)
        y, orig_sr = librosa.load(input_file, sr=target_sample_rate, mono=True)
        
        # Note: When sr is specified in librosa.load(), resampling happens automatically.
        # The 'y' variable is already at the 'target_sample_rate'.

        # Convert the audio array to a 16-bit integer format suitable for WAV file
        y_int16 = np.array(y * 32767, dtype=np.int16)

        # Save the downsampled audio to a new WAV file
        return wavfile.write(output_file, target_sample_rate, y_int16)

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
# Replace 'your_input.wav' with your actual file path, and adjust the target rate if needed.
# Common target rates are 16000 Hz for speech or 22050 Hz for general audio.

