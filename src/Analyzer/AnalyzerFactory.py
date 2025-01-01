import importlib.util
from pathlib import Path

class AnalyzerFactory:
    """Factory to create an Analyzer for making predictions on audio data.
    """

    @staticmethod
    def get_analyzer():
        """Getting an analyzer based on ml model to run predictions
        based on installed packages on the host.
        Returns
        -------
        x_model : TfModel or TfLiteModel
            The TfModel with full tensorflow model when tensorflow
            is installed on the host or the
            TfLiteModel with light version of tensorflow model 
            for embedded systems if tflite_runtime is installed on the host.
        Raises
        -------
        ImportError : If no expected installed package is available on the host
        """
        if importlib.util.find_spec("tensorflow"):
            from .TfModel import TfModel
            model_filename = Path.cwd() / "../model/out/model.h5"
            return TfModel(model_filename)
        elif importlib.util.find_spec("tflite_runtime"):
            from .TfLiteModel import TfLiteModel
            model_filename = Path.cwd() / "../model/out/model_light.tflite"
            return TfLiteModel(model_filename)
        else: raise ImportError("Expected tensorflow or tflite_runtime module installed.")