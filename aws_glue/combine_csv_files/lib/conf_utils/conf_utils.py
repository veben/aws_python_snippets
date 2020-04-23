from os import path, getcwd
from typing import List

from yaml import safe_load


def get_conf_file_path() -> str:
    return path.join(getcwd(), "resources/conf.yml")


def get_s3_result_folder_path() -> str:
    with open(get_conf_file_path(), "r") as ymlfile:
        return safe_load(ymlfile)["aws"]["s3"]["result-folder-path"]


def get_database_name() -> str:
    with open(get_conf_file_path(), "r") as ymlfile:
        return safe_load(ymlfile)["aws"]["glue"]["database"]


def get_table_v1_name() -> str:
    with open(get_conf_file_path(), "r") as ymlfile:
        return safe_load(ymlfile)["aws"]["glue"]["table-v1"]


def get_table_v2_name() -> str:
    with open(get_conf_file_path(), "r") as ymlfile:
        return safe_load(ymlfile)["aws"]["glue"]["table-v2"]


def get_final_columns_names() -> List[str]:
    with open(get_conf_file_path(), "r") as ymlfile:
        return safe_load(ymlfile)["columns"]
