import configparser


def sanitize_string(string: str):
    """Clean text from forbidden characters."""
    return string.replace("\n", "\\n")


class TokenNotValidError(Exception):
    pass


def load_config():
    """Load config to main scope of app."""
    config = configparser.ConfigParser()
    config.read("settings.toml")
    settings = dict()
    settings["host"] = config["DEFAULT"].get("host")
    settings["log_file_name"] = config["DEFAULT"].get("logfile")
    settings["reader_port"] = config["READER"].get("port")
    settings["sender_port"] = config["SENDER"].get("port")
    return settings
