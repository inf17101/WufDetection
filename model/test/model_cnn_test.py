import pytest
from tensorflow.keras.models import load_model

import librosa
import numpy as np
import random
    
def pad_trunc(aud, max_ms):
    sig, sr = aud
    num_rows = 1
    sig_len = sig.shape[0]
    max_len = sr//1000 * max_ms

    if (sig_len > max_len):
      # Truncate the signal to the given length
      sig = sig[:max_len]

    elif (sig_len < max_len):
      # Length of padding to add at the beginning and end of the signal
      pad_begin_len = random.randint(0, max_len - sig_len)
      pad_end_len = max_len - sig_len - pad_begin_len
      sig = np.pad(sig, (pad_begin_len, pad_end_len))
      
    return (sig, sr)

def extract_feature(file_name):
   
    try:
        audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast') 
        padded_audio, sr = pad_trunc((audio, sample_rate), 4000)
        melspec = librosa.feature.melspectrogram(y=padded_audio, sr=sr, n_mels=64, n_fft=1024)
        spec_melscale = librosa.power_to_db(melspec)
        melnormalized = librosa.util.normalize(spec_melscale)
        spec = np.expand_dims(melnormalized, axis=-1)
    except Exception:
        print("Error encountered while parsing file: ", file_name)
        return None

    return np.array([spec])

def prediction(model, file_name):
    prediction_feature = extract_feature(file_name)
    predicted_class = model.predict(prediction_feature)
    print(predicted_class)
    return np.round(predicted_class).reshape(-1)

@pytest.fixture
def model(scope="module"):
    model = load_model("../out/model_cnn.h5")
    return model

def test_no_bark(model):
    assert 0 == prediction(model, "../data/UrbanSound8K/audio/fold1/7061-6-0-0.wav")
    assert 0 == prediction(model, "../data/UrbanSound8K/audio/fold2/14387-9-0-19.wav")
    assert 0 == prediction(model, "../data/UrbanSound8K/audio/fold2/201652-5-2-3.wav")
    assert 0 == prediction(model, "../data/UrbanSound8K/audio/fold2/14387-9-0-7.wav")
    assert 0 == prediction(model, "../data/UrbanSound8K/audio/fold7/6902-2-0-5.wav")

def test_bark(model):
    assert 1 == prediction(model, "../data/bark.wav")
    assert 1 == prediction(model, "../data/UrbanSound8K/audio/fold5/66587-3-2-0.wav")