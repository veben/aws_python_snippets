from unittest import TestCase

from boto3 import Session
from moto import mock_s3

from list_buckets import get_all_s3_buckets

BUCKET_NAME = 'mocked_bucket'
S3_CLIENT = Session().client('s3')


@mock_s3
class TestFileUtils(TestCase):

    def setUp(self):
        S3_CLIENT.create_bucket(Bucket=BUCKET_NAME)

    def tearDown(self):
        S3_CLIENT.delete_bucket(Bucket=BUCKET_NAME)

    def test_get_all_s3_buckets(self):
        # when
        bucket_list = get_all_s3_buckets(S3_CLIENT)['Buckets']

        # then
        self.assertEqual(1, len(bucket_list))
        self.assertEqual(BUCKET_NAME, bucket_list[0]["Name"])
