"""Class for loading API configuration.
"""
import yaml

from api.config.constants import *

# Test


def load_config() -> dict:
    with open(CONFIG_PATH) as yaml_file:
        conf = yaml.load(yaml_file.read(), Loader=yaml.SafeLoader)
    return conf


# Global members
CONFIG = load_config()
