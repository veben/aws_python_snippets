from boto3.session import Session
from botocore.exceptions import ProfileNotFound, ClientError
from lib_pushing.conf_utils.conf_utils import get_default_region_name


S3_SERVICE_NAME = 's3'


def get_session_for_profile(profile: str) -> Session:
    try:
        return Session(profile_name=profile)
    except ProfileNotFound:
        print(f"The config profile {profile} could not be found, check your .aws configuration folder")
        raise


# Recover region from aws config files if available else default region
def get_bucket_region(session: Session) -> str:
    region = session.region_name
    return region if region is not None else get_default_region_name()


def check_s3_bucket_accessibility(aws_session: Session, bucket_name: str):
    try:
        aws_session.client(S3_SERVICE_NAME).head_bucket(Bucket=bucket_name)
    except ClientError:
        print(f"The bucket named <{bucket_name}> does not exist, or you dont' have permission to access it")
        raise


def upload_file_to_s3_bucket(aws_session: Session,
                             local_file_path: str,
                             bucket_name: str,
                             remote_file_path: str):
    aws_session.client(S3_SERVICE_NAME).upload_file(local_file_path, bucket_name, remote_file_path)
