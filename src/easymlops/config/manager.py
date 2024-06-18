import os
import yaml
from pathlib import Path

def find_config_file():
    ''' Load the easymlops.yaml config file in order: CWD, HOME '''

    potential_paths = []
    potential_paths.append(os.path.join(os.getcwd(), "easymlops.yaml"))
    potential_paths.append(os.path.join(str(Path.home()), "easymlops.yaml"))

    for path in potential_paths:
        if os.path.exists(path) and os.access(path, os.R_OK):
            break
    else:
        path = None

    return path

class ConfigManager(object):

    def __init__(self, config_path=None):
        self.config_path = config_path

        if self.config_path is None:
            self.config_path = find_config_file()
        if self.config_path is None:
            raise ValueError("Failed to find the config file in any of the potential paths.")

        with open(self.config_path) as f:
            self.conf = yaml.full_load(f)

    def get_config_value(self, key):
        return self.conf[key]

