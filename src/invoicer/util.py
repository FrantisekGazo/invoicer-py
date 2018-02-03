import yaml


def load_yaml(path):
    with open(path, 'r') as file:
        try:
            return yaml.load(file)
        except yaml.YAMLError as exc:
            print(exc)
