import os

import yaml


def get_addon_version():
    current_dir = os.path.dirname(__file__)
    config_path = os.path.join(current_dir, "..", "..", "config.yaml")
    normalized_path = os.path.normpath(config_path)

    with open(normalized_path, "r") as file:
        config = yaml.safe_load(file)
        return config.get("version")
