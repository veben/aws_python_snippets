from typing import Collection

import boto3
from boto3.session import Session


def get_all_s3_buckets(s3_client: Session.client) -> dict:
    # method 1
    return s3_client.list_buckets()


def print_all_bucket(buckets: dict):
    print('Existing buckets:')
    for bucket in buckets['Buckets']:
        print(f'  {bucket["Name"]}')


def get_all_s3_buckets_v2(s3_resource: Session.resource) -> Collection:
    # method 1
    return s3_resource.buckets.all()


def print_all_bucket_v2(buckets: Collection):
    print('Existing buckets:')
    for bucket in buckets:
        print(f'  {bucket.name}')


def main():
    session = boto3.Session(profile_name='p-dev')

    # session = boto3.Session(
    #     aws_access_key_id=settings.AWS_SERVER_PUBLIC_KEY,
    #     aws_secret_access_key=settings.AWS_SERVER_SECRET_KEY,
    # )

    print_all_bucket(get_all_s3_buckets(session.client('s3')))
    print_all_bucket_v2(get_all_s3_buckets_v2(session.resource('s3')))


if __name__ == "__main__":
    main()
