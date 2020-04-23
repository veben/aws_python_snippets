import os
from datetime import datetime
from typing import List

from boto3.session import Session

from lib.aws_client.aws_client import upload_file_to_s3_bucket


def get_local_files_folder_path() -> str:
    return os.path.join(os.getcwd(), "resources\\files")


def get_all_file_names(folder_path: str) -> List[str]:
    return os.listdir(folder_path)


def get_folder_name_from_current_datetime() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H:%M:%S")


def get_folder_name_from_filename(filename: str) -> str:
    try:
        return filename[0:11]
    except IndexError:
        print(f"The filename <{filename}> is incorrect")


def upload_local_file(aws_session: Session, local_folder_path: str, bucket_name: str, remote_parent_folder_name: str,
                      filename: str):
    remote_nested_folder_name = get_folder_name_from_filename(filename)
    upload_file_to_s3_bucket(aws_session,
                             local_folder_path + '/' + filename,
                             bucket_name,
                             remote_parent_folder_name + '/' + remote_nested_folder_name + '/' + filename)


def upload_local_files(aws_session: Session, bucket_name: str):
    local_folder_path = get_local_files_folder_path()

    remote_parent_folder_name = get_folder_name_from_current_datetime()

    for filename in get_all_file_names(local_folder_path):
        upload_local_file(aws_session, local_folder_path, bucket_name, remote_parent_folder_name, filename)
