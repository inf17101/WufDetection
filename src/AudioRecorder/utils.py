import io, wave
"""Useful utilities to convert and preprocess audio data.
"""


def audio_to_wave(raw_audio, rate, channels, sample_width):
    """Takes audio data and creates an in-memory wav file out of it
    Parameters
    ----------
    raw_audio : bytes or numeric values
        The numeric-valued audio data buffer
    rate : int
        The sample rate of ``raw_audio``
    channels : numeric type
        The number of channels of ``raw_audio``
    sample_width: int [1, 2, 3]
        The interpretation format (bit-width) of the audio data.
    Returns
    -------
    x_bytes : bytes
        The container of bytes representing wav file
    """
    temp_file = io.BytesIO()
    with wave.open(temp_file, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(raw_audio)

    temp_file.seek(0)
    return temp_file.read()