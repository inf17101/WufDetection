from Analyzer.AnalyzerFactory import AnalyzerFactory
from AudioRecorder.AudioRecorder import AudioRecorder
from AudioRecorder.utils import audio_to_wave
from Analyzer.AudioAnalyzer import AudioAnalyzer
from Queue.Queue import Queue
from ResultPublisher.ResultPublisher import ResultPublisher
from ConfigReader.ConfigReader import ConfigReader
from threading import Thread, Event
import time, copy

def record_and_store(queue, event, config):
    """Records audio from an input stream (microphone)
    and stores the read-in audio data into queue.
    Stops when event is set or exception is raised.
    The code is designed to run inside an own thread.
    Parameters
    ----------
    queue : Queue
        The queue containing raw audio data
    event : Event
        The event condition variable to determine when to stop
    config : dict
        The config for analyzing and publishing
    """

    try:
        channels = int(config["RECORDER"]["channels"])
        rate = int(config["RECORDER"]["sample_rate"])
        duration = int(config["RECORDER"]["duration"])
        chunk_size = int(config["RECORDER"]["chunk_size"])
        recorder = AudioRecorder(rate, duration, chunk_size, channels)
        while event.is_set():
            frames = recorder.next_audiodata()
            queue.put(frames)
            print(f"Buffer size after putting item in: {queue.current_size()}")
    except Exception as e:
        print("Error in recording thread:", e)
        event.clear()

def analyze_audio_and_publish_result(queue, event, config):
    """Read the audio data of the queue,
    analyzing the audio and making predictions with ml model
    and publish analyzing results to messenger service.
    Stops when event is set or exception is raised.
    The code is designed to run inside an own thread.
    Parameters
    ----------
    queue : Queue
        The queue containing raw audio data
    event : Event
        The event condition variable to determine when to stop
    config : dict
        The config for analyzing and publishing
    """

    try:
        threshold = float(config["ANALYZER"]["threshold"])
        sample_rate = int(config["RECORDER"]["sample_rate"])
        channels = int(config["RECORDER"]["channels"])
        startup_msg = config["PUBLISHER"]["startup_msg"]
        title = config["PUBLISHER"]["title_bark_audio"]
        msg = config["PUBLISHER"]["msg"]
        token = config["PUBLISHER"]["token"]
        chat_id = config["PUBLISHER"]["chat_id"]
        retries = int(config["PUBLISHER"]["max_retries"])

        analyzer = AudioAnalyzer(AnalyzerFactory.get_analyzer())
        publisher = ResultPublisher(token, chat_id, retries)
        
        publisher.get_updates()
        publisher.publish(startup_msg)
        while event.is_set():
            raw_data = queue.pop()
            result = analyzer.analyze(raw_data, sample_rate, threshold=threshold)
            queue.task_done()
            print(f"Analyzer result: {result}")
            if result:
                publisher.publish_audiodata(
                    audio_to_wave(raw_data, sample_rate, channels, sample_width=2),
                    title=f"{title}.wav",
                    caption=msg
                )
    except Exception as e:
        print("Error in analyzing thread:", e)
        event.clear()


def main():
    """Main program of application.
    Read in the config of config file for application.
    Initializes a queue.
    Setting up two threads, one for producing audio data and
    the other one for anaylzing it and publishing result to
    messenger service.
    Checks periodically for KeyboardInterrupt (Strg + C) and
    terminates the program if KeyboardInterrupt is happening.
    """
    config = ConfigReader.read("../config.conf")
    queue = Queue(int(config["QUEUE"]["q_size"]))
    event = Event()
    event.set()
    thread_input = Thread(target=record_and_store, args=(queue, event, config), daemon=True)
    thread_output = Thread(target=analyze_audio_and_publish_result, args=(queue, event, copy.deepcopy(config)), daemon=True)
    thread_input.start()
    thread_output.start()

    try:
        while event.is_set():
            time.sleep(0.5)
    except KeyboardInterrupt:
        event.clear()
        thread_input.join()
        thread_output.join()
        print("Closed all worker threads successfully.")


if __name__ == "__main__":
    exit(main())
