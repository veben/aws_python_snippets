from unittest import TestCase

from lib_crawling.conf_utils.conf_utils import get_crawler_name, get_database_name, get_default_region_name, \
    get_profile_name, get_s3_folder_path


class TestFileUtils(TestCase):

    def test_get_profile_name(self):
        self.assertEqual("p-dev", get_profile_name())

    def test_get_default_region_name(self):
        self.assertEqual("eu-west-1", get_default_region_name())

    def test_get_s3_folder_path(self):
        self.assertEqual("s3://aws-glue-pokemon-csv/2020-04-23_13:59:42", get_s3_folder_path())

    def test_get_database_name(self):
        self.assertEqual("pokemons", get_database_name())

    def test_get_crawler_name(self):
        self.assertEqual("pokemon-csv-crawler", get_crawler_name())
