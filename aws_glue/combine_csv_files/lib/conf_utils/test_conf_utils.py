from unittest import TestCase

from aws_glue.combine_csv_files.lib.conf_utils.conf_utils import get_database_name, get_table_v1_name, \
    get_table_v2_name, get_final_columns_names, get_s3_result_folder_path


class TestFileUtils(TestCase):

    def test_get_s3_result_folder_path(self):
        self.assertEqual("s3://aws-glue-pokemon-tmp/csv_file_result/", get_s3_result_folder_path())

    def test_get_database_name(self):
        self.assertEqual("pokemons", get_database_name())

    def test_get_table_v1_name(self):
        self.assertEqual("pokemons_v1", get_table_v1_name())

    def test_get_table_v2_name(self):
        self.assertEqual("pokemons_v2", get_table_v2_name())

    def test_get_final_columns_names(self):
        self.assertEqual([
            'id',
            'identifier',
            'generation',
            'first_type',
            'second_type',
            'legendary',
            'base_experience',
            'attack',
            'defense',
            'hp',
            'speed'], get_final_columns_names())
