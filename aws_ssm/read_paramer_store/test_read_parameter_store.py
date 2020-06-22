from unittest import TestCase

from boto3 import Session
from moto import mock_ssm

from read_parameter_store import read_parameter_store

SSM_CLIENT = Session().client('ssm')
PARAMETER_NAME = '/config/db/name'
PARAMETER_VALUE = 'my_db'


@mock_ssm
class TestFileUtils(TestCase):
    def setUp(self):
        SSM_CLIENT.put_parameter(
            Name=PARAMETER_NAME,
            Description="A test parameter",
            Value=PARAMETER_VALUE,
            Type="SecureString",
        )

    def tearDown(self):
        SSM_CLIENT.delete_parameter(Name=PARAMETER_NAME)

    def test_read_parameter_store(self):
        # when
        param_value = read_parameter_store(SSM_CLIENT, PARAMETER_NAME)

        # then
        self.assertEqual(PARAMETER_VALUE, param_value)