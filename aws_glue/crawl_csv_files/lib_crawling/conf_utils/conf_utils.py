from os import path, getcwd

from yaml import safe_load


def get_profile_name() -> str:
    with open(get_conf_file_path(), "r") as ymlfile:
        return safe_load(ymlfile)["aws"]["profile"]


def get_default_region_name() -> str:
    with open(get_conf_file_path(), "r") as ymlfile:
        return safe_load(ymlfile)["aws"]["default-region"]


def get_conf_file_path() -> str:
    return path.join(getcwd(), "resources/conf.yml")


def get_s3_folder_path() -> str:
    with open(get_conf_file_path(), "r") as ymlfile:
        return safe_load(ymlfile)["aws"]["s3"]["folder-path"]


def get_database_name() -> str:
    with open(get_conf_file_path(), "r") as ymlfile:
        return safe_load(ymlfile)["aws"]["glue"]["database"]


def get_crawler_name() -> str:
    with open(get_conf_file_path(), "r") as ymlfile:
        return safe_load(ymlfile)["aws"]["glue"]["crawler-name"]
