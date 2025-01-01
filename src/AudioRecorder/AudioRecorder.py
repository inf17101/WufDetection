import pyaudio

class AudioRecorder:
    """Records audio data from input devices.
    The raw audio data can be used by other modules to process
    and use the audio data
    """

    def __init__(self, rate=44100, duration=4, chunk=2048,channels=1,format=pyaudio.paInt16):
        """Records audio based on passed input parameters.
        Opens Audio stream based on the passed parmeters 
        and stores the started audio stream as member.
        Parameters
        ----------
        rate : int
            The sampling rate of the input device for recording audio
        duration : int
            The duration of the audio recording
        chunk : int
            The chunk size for processing the input stream audio data in chunks (default: 2048)
        channels : int
            The amount of channels to record (default: 1 [mono])
        format : pyaudio.pa[Format]
            The interpretation format of audio data in the buffer (default: int 16 bit)
        """

        self.__rate = rate
        self.__duration = duration
        self.__chunk = chunk
        self.__channels = channels
        self.__format = format
        self.__audio = pyaudio.PyAudio()
        self.__stream = self.__audio.open(format=self.__format,
                        channels=self.__channels,
                        rate=self.__rate,
                        input=True, frames_per_buffer=self.__chunk)

    def __del__(self):
        """Stops the audio recording stream and cleans up the stream object.
        """

        self.__stream.stop_stream()
        self.__stream.close()
        self.__audio.terminate()

    def next_audiodata(self):
        """Getting the next available audio data of the input stream
        Reads in and returns the raw audio data from the stream as bytes according to
        the specified duration
        Returns
        -------
        x_bytes : byte
            Recorded audio data as bytes
        """
        
        frames = []
        for _ in range(int(self.__rate / self.__chunk * self.__duration)):
            data = self.__stream.read(self.__chunk)
            frames.append(data)
        return b''.join(frames)