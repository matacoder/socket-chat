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
    settings = {
        "host": config["DEFAULT"].get("host"),
        "log_file_name": config["DEFAULT"].get("logfile"),
        "reader_port": config["READER"].get("port"),
        "sender_port": config["SENDER"].get("port"),
    }
    return settings
