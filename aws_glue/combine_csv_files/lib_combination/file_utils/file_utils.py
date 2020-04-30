import os


def get_local_script_folder_path() -> str:
    return os.path.join(os.getcwd(), "resources\\scripts")
