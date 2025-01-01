import pytest
from tensorflow.keras.models import load_model

import librosa
import numpy as np

def extract_feature(file_name):
   
    try:
        audio_data, sample_rate = librosa.load(file_name, res_type='kaiser_fast')
        mfccs = librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=40)
        mfccsscaled = np.mean(mfccs.T,axis=0)
    except Exception:
        print("Error encountered while parsing file: ", file_name)
        return None

    return np.array([mfccsscaled])

def prediction(model, file_name):
    prediction_feature = extract_feature(file_name)
    predicted_class = model.predict(prediction_feature)
    print(predicted_class)
    return np.round(predicted_class).reshape(-1)

@pytest.fixture
def model(scope="module"):
    model = load_model("../out/model.h5")
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