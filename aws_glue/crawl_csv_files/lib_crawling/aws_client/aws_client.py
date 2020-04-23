from boto3 import Session
from botocore.exceptions import ProfileNotFound

from lib_crawling.conf_utils.conf_utils import get_default_region_name


def get_session_for_profile(profile: str) -> Session:
    try:
        return Session(profile_name=profile)
    except ProfileNotFound:
        print(f"The config profile {profile} could not be found, check your .aws configuration folder")
        raise


# Recover region from aws config files if available else default region
def get_region(session: Session) -> str:
    region = session.region_name
    return region if region is not None else get_default_region_name()


def create_crawler(glue_client: Session.client, crawler_name: str, database_name: str, remote_folder_path: str) -> dict:
    return glue_client.create_crawler(Name=crawler_name,
                                      Role='AWSGlueServiceRoleDefault',
                                      DatabaseName=database_name,
                                      Targets={'S3Targets': [{'Path': remote_folder_path}]})


def update_crawler(glue_client: Session.client, crawler_name: str, remote_folder_path: str) -> dict:
    return glue_client.update_crawler(Name=crawler_name, Targets={'S3Targets': [{'Path': remote_folder_path}]})


def define_crawler(glue_client: Session.client, crawler_name: str, database_name: str, remote_folder_path: str) -> dict:
    response: dict
    try:
        response = update_crawler(glue_client, crawler_name, remote_folder_path)
        print(f"Update crawler <{crawler_name}> to <{remote_folder_path}> remote path")
    except glue_client.exceptions.EntityNotFoundException:
        response = create_crawler(glue_client, crawler_name, database_name, remote_folder_path)
        print(f"Create crawler <{crawler_name}> on <{database_name}> database to <{remote_folder_path}> remote path")

    return response


def crawl(glue_client: Session.client, crawler_name) -> dict:
    return glue_client.start_crawler(Name=crawler_name)
