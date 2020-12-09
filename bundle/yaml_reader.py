import os
import yaml

YAML_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)))


def get_confs():
    with open(YAML_PATH + '/accounts.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return data
