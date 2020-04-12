"""Class for loading API configuration.
"""
import yaml

# Test
def load_config() -> dict:
    with open('./backend/core/config/config.yml', 'r') as yaml_file:
        conf = yaml.load(yaml_file.read(), Loader=yaml.SafeLoader)
    return conf


# Global members
CONFIG = load_config()
