from pathlib import Path
from unittest import TestCase
from boto3 import Session
from moto import mock_s3

from lib_pushing.aws_client.aws_client import S3_SERVICE_NAME, upload_file_to_s3_bucket


class TestFileUtils(TestCase):

    @mock_s3
    def test_upload_file_to_s3_bucket(self):
        # given
        bucket_name = 'mocked_bucket'
        filename = "pokemons_v1.csv"
        session = Session()
        s3_client = session.client(S3_SERVICE_NAME)
        s3_client.create_bucket(Bucket=bucket_name)

        # when
        upload_file_to_s3_bucket(session,
                                 str(Path(__file__).parent) + "\\resources\\files" + "/" + filename,
                                 bucket_name,
                                 "files" + "/" + filename)

        # then
        self.assertEqual(1, len(s3_client.list_objects(Bucket=bucket_name)['Contents']))
