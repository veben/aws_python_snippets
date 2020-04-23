from unittest import TestCase
from lib_pushing.conf_utils.conf_utils import get_profile_name, get_default_region_name, get_bucket_name


class TestFileUtils(TestCase):

    def test_get_profile_name(self):
        self.assertEqual("p-dev", get_profile_name())

    def test_get_default_region_name(self):
        self.assertEqual("eu-west-1", get_default_region_name())

    def test_get_bucket_name(self):
        self.assertEqual("aws-glue-pokemon-csv", get_bucket_name())
