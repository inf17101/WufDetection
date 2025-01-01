import configparser

def default_format(config) -> dict:
    """Default parsing and formatting the config.
    Constructs a dictionary of sections and key-value pairs
    but removes the comments of the lines.
    Parameters
    ----------
    config : configparser.ConfigParser
        The config object
    Returns
    ----------
    x_dict : dict
        Dictionary containing all sections and key-value pairs
        of the config file without comments in the config file.
    """

    result_config = {}
    for s in config.sections():
        items = dict(config.items(s))
        for key, value in items.items():
            pos = value.find("#")
            if pos > 0:
                value = value[:pos].strip()
            items[key] = value.strip()
        result_config[s] = items
    return result_config

class ConfigReader:
    """Read in the config of the application."""

    @staticmethod
    def read(filepath, format_func=default_format) -> dict:
        """Read in the config for the application.
        Parameters
        ----------
        filepath : string
            The filepath of the config
        format_func : int
            The custom format function to format the values
            before returning them (default: default_format)
        Returns
        ----------
        x_dict : dict
            Dictionary containing all sections and key-value pairs
            of the config file.
        """
        
        config = configparser.ConfigParser()
        config.read(filepath)
        if format_func:
            return format_func(config)
        else:
            return {s:dict(config.items(s)) for s in config.sections()}