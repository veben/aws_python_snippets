from lib_combination.aws_client.aws_client import get_session_for_profile, run_job, get_job, create_job
from lib_combination.aws_client.aws_client import upload_file_to_s3_bucket
from lib_combination.conf_utils.conf_utils import get_job_name, get_profile_name, get_bucket_name, get_database_name
from lib_combination.file_utils.file_utils import get_local_script_folder_path


def main():
    profile_name = get_profile_name()
    aws_session = get_session_for_profile(profile_name)
    job_name = get_job_name()
    bucket_name = get_bucket_name()
    base_name = get_database_name()
    script_name = 'pokemon-v1-v2-combination.py'
    local_script_sub_path = get_local_script_folder_path() + '/' + script_name
    remote_script_sub_path = 'combination/scripts' + '/' + script_name
    remote_script_location = "s3://" + bucket_name + "/" + remote_script_sub_path
    remote_result_file_full_path = "s3://" + bucket_name + "/combination/csv_file_result_job"
    remote_tmp_files_path = "s3://" + bucket_name + "/combination/tmp"

    glue_client = aws_session.client('glue')

    upload_file_to_s3_bucket(aws_session,
                             local_script_sub_path,
                             bucket_name,
                             remote_script_sub_path)

    job: dict
    try:
        job = get_job(glue_client, job_name)
    except glue_client.exceptions.EntityNotFoundException:
        job = create_job(glue_client, job_name, remote_script_location, remote_result_file_full_path, base_name,
                         remote_tmp_files_path)
        print(f"Create job <{job_name}>")

    if job['ResponseMetadata']['HTTPStatusCode'] == 200:
        print(f"Run job <{job_name}>"
              f"with <{profile_name}> profile...")

        run_job(glue_client, job_name, remote_result_file_full_path, base_name)
    else:
        print(f"Error to define <{job_name}> job")


if __name__ == "__main__":
    main()
