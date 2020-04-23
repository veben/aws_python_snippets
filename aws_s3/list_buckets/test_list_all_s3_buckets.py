from unittest import TestCase

from boto3 import Session
from moto import mock_s3

from list_all_s3_buckets import get_all_s3_buckets

BUCKET_NAME = 'mocked_bucket'


@mock_s3
class TestFileUtils(TestCase):

    def setUp(self):
        Session().client('s3').create_bucket(Bucket=BUCKET_NAME)

    def tearDown(self):
        Session().client('s3').delete_bucket(Bucket=BUCKET_NAME)

    def test_get_all_s3_buckets(self):
        # when
        bucket_list = get_all_s3_buckets()['Buckets']

        # then
        self.assertEqual(1, len(bucket_list))
        self.assertEqual(BUCKET_NAME, bucket_list[0]["Name"])

    # def test_get_all_s3_buckets_v2(self):
    #     # when
    #     bucket_collection = get_all_s3_buckets_v2()
    #
    #     # then
    #     self.assertEqual(1, len(bucket_collection))
    #     self.assertEqual(BUCKET_NAME, bucket_collection[0].name)
