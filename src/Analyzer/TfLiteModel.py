import tflite_runtime.interpreter as tflite

class TfLiteModel:
    """Tensorflow light model abstraction for usage of model
    on restricted systems like embedded devices.
    """

    def __init__(self, model_filename):
        """Loads ml model coverted in a lightweight tensorflow ml model format.
        Parameters
        ----------
        model_filename : Path
            The path to the tflite model.
        """
        self.__model = tflite.Interpreter(model_path=str(model_filename))
        self.__model.allocate_tensors() 
        self.__input_details = self.__model.get_input_details()
        self.__output_details = self.__model.get_output_details()

    def predict(self, feature):
        """Run predictions on the loaded tflite ml model.
        Parameters
        ----------
        feature : int (40, x)
            The audio data features as input of the ml model
        Returns
        x_float: float (0.0 >= x_float <= 1.0)
            The probability of the prediction.
        ----------
        """
        self.__model.set_tensor(self.__input_details[0]["index"], feature)
        self.__model.invoke()
        return self.__model.get_tensor(self.__output_details[0]["index"])
