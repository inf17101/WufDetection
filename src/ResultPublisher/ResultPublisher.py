from urllib3 import PoolManager
from urllib3.util import Retry
import json

class ResultPublisher:
    """Publish results to instant messenger service."""

    def __init__(self, token, chat_id, retires):
        """Constructs ResultPublisher with settings.
        Parameters
        ----------
        token : string
            The access token to access messenger service.
        chat_id : int
            The chat id of the chat where to send messages into.
        retries : int
            The amount of retries when sending http requests
        """

        self.__token = token
        self.__chat_id = chat_id
        self.__urlMessage = f"https://api.telegram.org/bot{self.__token}/sendMessage?chat_id={self.__chat_id}&text="
        self.__urlAudio = f"https://api.telegram.org/bot{self.__token}/sendAudio"
        self.__urlUpdates = f"https://api.telegram.org/bot{self.__token}/getUpdates"
        self.__http = PoolManager(retries=Retry(retires, raise_on_status=False, status_forcelist=range(400, 600)))

    def response_success(self, status_code):
        """Checks if http response is successfull.
        Parameters
        ----------
        status_code : int
            The http status code
        Returns:
        ----------
        x_bool : bool
        """

        return status_code >= 200 and status_code <= 299

    def get_updates(self):
        """Get updates of the messenger service
        usually to fetch newest messages and for testing
        the connection to the messenger service
        Returns:
        ----------
        x_dict : dict
            The json reply of the messenger service as dictionary.
        """

        response = self.__http.request("GET", self.__urlUpdates)
        if self.response_success(response.status):
            return dict(json.loads(response.data.decode("utf-8")))
        return {}

    def publish(self, message):
        """Publish a message to the messenger service.
        Returns:
        ----------
        x_dict : dict
            The json reply of the messenger service as dictionary.
        """

        response = self.__http.request("GET", self.__urlMessage + message)
        if self.response_success(response.status):
            return dict(json.loads(response.data.decode("utf-8")))
        return {}

    def publish_audiodata(self, audio_data, title, caption=""):
        """Publish an audio file to the messenger service.
        Returns:
        ----------
        x_dict : dict
            The json reply of the messenger service as dictionary.
        """

        payload = {
            "chat_id": f"{self.__chat_id}",
            "caption": f"{caption}",
            "audio": (title, audio_data, "multipart/form-data")
        }

        response = self.__http.request("POST", self.__urlAudio, fields=payload)
        
        if self.response_success(response.status):
            return dict(json.loads(response.data.decode("utf-8")))
        return {}
