import queue

class Queue:
    """Storage for the raw audio data."""

    def __init__(self, size):
        """Initialize a queue based on a size.
        Parameters
        ----------
        size : int
            The size of the queue as a power of 2
        """
        self.__queue = queue.Queue(size)

    def put(self, data):
        """Put in data lock- and wait-free into the queue.
        Parameters
        ----------
        data : bytes
            The input data
        Returns
        ----------
        x_bool : bool
            True if data was inserted and
            False if queue is full.
        """
        try:
            self.__queue.put_nowait(data)
            return True
        except queue.Full:
            print("Queue is full.")
            return False

    def pop(self):
        """Pop data out of the queue.
        If queue is empty the caller is blocked
        until data is available.
        Returns
        ----------
        x_bytes : byte
            The data inside the queue and
            deletes it out of the queue.
        """
        return self.__queue.get()

    def task_done(self):
        """Mark task as done
        after reading it out of queue.
        """
        self.__queue.task_done()

    def current_size(self):
        """Getting the current size of the queue.
        Returns
        ----------
        x_int : int
            The current size of the queue.
        """
        return self.__queue.qsize()
