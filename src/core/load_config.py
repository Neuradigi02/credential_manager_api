import yaml


with open("config.yaml") as yaml_data_file:
    config = yaml.safe_load(yaml_data_file)
