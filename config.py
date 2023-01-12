import yaml


def get_config(section: str) -> dict:
    with open("config.yaml") as f:
        config = yaml.safe_load(f.read())
        f.close()
    return config[section]
