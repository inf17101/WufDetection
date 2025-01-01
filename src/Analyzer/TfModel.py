from tensorflow.keras.models import load_model

class TfModel:
    """Tensorflow full model abstraction for usage of model."""

    def __init__(self, model_filename):
        """Loads ml model coverted in a standard tensorflow ml model format.
        Parameters
        ----------
        model_filename : Path
            The path to the model.
        """
        self.__model = load_model(str(model_filename))


    def predict(self, feature):
        """Run predictions on the loaded ml model.
        Parameters
        ----------
        feature : int (40, x)
            The audio data features as input of the ml model
        Returns
        x_float: float (0.0 >= x_float <= 1.0)
            The probability of the prediction.
        ----------
        """
        return self.__model.predict(feature)
