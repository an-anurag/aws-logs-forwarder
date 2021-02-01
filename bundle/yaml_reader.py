import os
import yaml
from bundle.logger import logger

YAML_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)))


def get_confs():
    with open(YAML_PATH + '/accounts.yaml') as f:
        try:
            data = yaml.safe_load(f)
            return data
        except yaml.YAMLError as err:
            logger.exception(err, "Cannot read YAML configuration")
