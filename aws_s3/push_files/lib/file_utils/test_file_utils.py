from unittest import TestCase
from lib.file_utils.file_utils import get_all_file_names, get_local_files_folder_path, \
    get_folder_name_from_filename


CSV_FILE_NAMES = sorted(["pokemons_v1.csv", "pokemons_v1_2.csv", "pokemons_v2.csv"])


class TestFileUtils(TestCase):

    def test_get_all_file_names(self):
        self.assertEqual(CSV_FILE_NAMES,
                         sorted(get_all_file_names(get_local_files_folder_path())))

    def test_get_folder_name_from_filename_ok(self):
        self.assertEqual("pokemons_v1", get_folder_name_from_filename(CSV_FILE_NAMES[0]))
        self.assertEqual("pokemons_v1", get_folder_name_from_filename(CSV_FILE_NAMES[1]))
        self.assertEqual("pokemons_v2", get_folder_name_from_filename(CSV_FILE_NAMES[2]))
