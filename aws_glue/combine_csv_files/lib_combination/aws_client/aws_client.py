from boto3 import Session
from botocore.exceptions import ProfileNotFound

from lib_combination.conf_utils.conf_utils import get_default_region_name


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


def get_job(glue_client: Session.client, job_name: str) -> dict:
    return glue_client.get_job(JobName=job_name)


def create_job(glue_client: Session.client, job_name: str, remote_script_location: str,
               remote_result_file_full_path: str, base_name: str, remote_tmp_files_path: str) -> dict:
    return glue_client.create_job(
        Name=job_name,
        Role='AWSGlueServiceRoleDefault',
        Command={
            'Name': 'glueetl',
            'ScriptLocation': remote_script_location,
            'PythonVersion': '3'
        },
        DefaultArguments={
            '--result_bucket_path': remote_result_file_full_path,
            '--base': base_name,
            '--table_v1': 'pokemons_v1',
            '--table_v2': 'pokemons_v2',
            '--job-language': 'python',
            '--TempDir': remote_tmp_files_path
        },
        GlueVersion='1.0',
        Timeout=2880,
        MaxCapacity=10
    )


def define_job(glue_client: Session.client, job_name: str, remote_script_location: str) -> dict:
    response: dict
    try:
        response = get_job(glue_client, job_name)
    except glue_client.exceptions.EntityNotFoundException:
        response = create_job(glue_client, job_name, remote_script_location)
        print(f"Create job <{job_name}>")
    return response


def run_job(glue_client: Session.client, job_name: str, remote_result_file_full_path: str, base: str):
    glue_client.start_job_run(JobName=job_name,
                              Arguments={
                                  '--result_bucket_path': remote_result_file_full_path,
                                  '--base': base,
                                  '--table_v1': 'pokemons_v1',
                                  '--table_v2': 'pokemons_v2'})


def upload_file_to_s3_bucket(aws_session: Session,
                             local_file_path: str,
                             bucket_name: str,
                             remote_file_path: str):
    aws_session.client('s3').upload_file(local_file_path, bucket_name, remote_file_path)
