from lib_crawling.aws_client.aws_client import define_crawler, get_region, crawl
from lib_crawling.aws_client.aws_client import get_session_for_profile
from lib_crawling.conf_utils.conf_utils import get_profile_name, get_s3_folder_path, get_database_name, get_crawler_name


def main():
    profile_name = get_profile_name()
    aws_session = get_session_for_profile(profile_name)
    remote_folder_path = get_s3_folder_path()
    crawler_name = get_crawler_name()

    glue_client = aws_session.client('glue')

    response = define_crawler(glue_client, crawler_name, get_database_name(), remote_folder_path)

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print(f"Crawl "
              f"in <{get_region(aws_session)}> region, "
              f"with <{profile_name}> profile, "
              f"from <{remote_folder_path}> s3 bucket path...")

        crawl(glue_client, crawler_name)
    else:
        print(f"Error to define <{crawler_name}> crawler")


if __name__ == "__main__":
    main()
