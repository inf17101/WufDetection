import librosa
import numpy as np

class AudioAnalyzer:
    """Analyzes audio data and runs predictions on the
    audio data based on a passed-in ml model.
    """

    def __init__(self, model):
        """Constructs AudioAnalyzer object.
        Parameters
        ----------
        model : ml model
            The ml model of for example tensorflow or tensorflow light
        """
        
        self.__model = model

    def __buf_to_float(self, x, *, n_bytes=2, dtype=np.float32):
        """Convert an integer buffer to floating point values.
        This is primarily useful when loading integer-valued wav data
        into numpy arrays.
        Parameters
        ----------
        x : np.ndarray [dtype=int]
            The integer-valued data buffer
        n_bytes : int [1, 2, 4]
            The number of bytes per sample in ``x``
        dtype : numeric type
            The target output type (default: 32-bit float)
        Returns
        -------
        x_float : np.ndarray [dtype=float]
            The input data buffer cast to floating point
        """

        # Invert the scale of the data
        scale = 1.0 / float(1 << ((8 * n_bytes) - 1))

        # Construct the format string
        fmt = "<i{:d}".format(n_bytes)

        # Rescale and format the data buffer
        return scale * np.frombuffer(x, fmt).astype(dtype)

    def analyze(self, raw_data, orig_sr, threshold=0.95, target_sr=22050, n_mfcc=40) -> bool:
        """Runs prediction with ml model on audio data returns result
        Takes raw audio data, preprocesses the audio data
        to fit the input type of the ml model and runs prediction on the audio data.
        Returns True if prediction result (probability) is greater than the passed
        threshold, False otherwise.
        Parameters
        ----------
        raw_data : byte
            The raw audio data as bytes
        orig_sr : int
            The original sampling rate of ``raw_data``
        threshold : float
            The threshold for prediction result as probability (default: 0.95)
        target_sr : int
            The target sampling rate of the audio data for ml model input (default: 22050)
        n_mfcc : int
            The number of mfccs that should be calculated of the audio data (default: 40)
        Returns
        -------
        x_bool : bool
            True if probability of model prediction is greater than 
            defined threshold or False otherwise
        """

        audio_data = self.__buf_to_float(raw_data)
        resampled_audio = librosa.resample(
            audio_data, orig_sr=orig_sr, target_sr=target_sr, res_type='kaiser_fast')
        mfccs = librosa.feature.mfcc(
            y=resampled_audio, sr=target_sr, n_mfcc=n_mfcc)
        mfccsscaled = np.mean(mfccs.T, axis=0)
        feature = np.array([mfccsscaled])
        predicted_class = self.__model.predict(feature)
        probability = predicted_class.reshape(-1)[0]
        print("Analyzing result:", probability)
        if probability > threshold:
            return True
        return False
