from lib.aws_client.aws_client import get_session_for_profile, check_s3_bucket_accessibility, get_bucket_region
from lib.conf_utils.conf_utils import get_profile_name, get_bucket_name
from lib.file_utils.file_utils import upload_local_files


def main():
    profile_name = get_profile_name()
    bucket_name = get_bucket_name()
    aws_session = get_session_for_profile(profile_name)

    check_s3_bucket_accessibility(aws_session, bucket_name)

    print(f"Uploading files "
          f"to <{get_bucket_region(aws_session)}> region, "
          f"with <{profile_name}> profile, "
          f"in <{bucket_name}> s3 bucket")

    upload_local_files(aws_session, bucket_name)


if __name__ == "__main__":
    main()
