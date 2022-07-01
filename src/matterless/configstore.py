import configparser
import os


def load_config(configfile: str) -> configparser.ConfigParser:
    """Load config file."""
    config = configparser.ConfigParser()
    config.read(configfile)
    return config


def save_config(configfile: str, config: configparser.ConfigParser) -> None:
    """Save config file."""
    os.makedirs(os.path.dirname(configfile), exist_ok=True)
    for sectionname, section in config.items():
        for setting, value in section.items():
            if not value:
                config.remove_option(sectionname, setting)

    with open(configfile, "w") as f:
        config.write(f)
