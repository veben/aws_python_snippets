from os import path, getcwd

from yaml import safe_load


def get_profile_name() -> str:
    with open(get_conf_file_path(), "r") as ymlfile:
        return safe_load(ymlfile)["aws"]["profile"]


def get_default_region_name() -> str:
    with open(get_conf_file_path(), "r") as ymlfile:
        return safe_load(ymlfile)["aws"]["default-region"]


def get_bucket_name() -> str:
    with open(get_conf_file_path(), "r") as ymlfile:
        return safe_load(ymlfile)["aws"]["bucket-name"]


def get_conf_file_path() -> str:
    return path.join(getcwd(), "resources/conf.yml")


def get_database_name() -> str:
    with open(get_conf_file_path(), "r") as ymlfile:
        return safe_load(ymlfile)["aws"]["glue"]["database"]


def get_job_name() -> str:
    with open(get_conf_file_path(), "r") as ymlfile:
        return safe_load(ymlfile)["aws"]["glue"]["job-name"]
