from db_operations import *
import unittest
from unittest.mock import MagicMock, patch
import sys
# setting path
sys.path.append('../music_db')


class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Create a mock engine and session for testing
        self.mock_engine = MagicMock()
        self.mock_session = MagicMock()

        self.db_instance = Database()
        self.db_instance.engine = self.mock_engine
        self.db_instance.session = self.mock_session

    def tearDown(self) -> None:
        self.db_instance.session.close()
        return super().tearDown()

    def test_add_entry(self):
        with patch('db_operations.Band') as mock_band_class:
            result = self.db_instance.add_entry('bands', {'name': 'Test Band'})
            result_no_table = self.db_instance.add_entry(
                'wrong_table', {'name': 'Test Band'})
            result_wrong_column = self.db_instance.add_entry(
                'bands', {'wrong_col': 'Test Band'})

            self.assertEqual(
                result_no_table, "Table (wrong_table) does not exist.")
            self.assertEqual(
                result_wrong_column, "Can't add the entry to the database, there's no column wrong_col in table bands")
            self.assertEqual(result, "Added entry to the (bands) table.")

    def test_update_entry(self):
        with patch('db_operations.Database') as mock_db_class:
            self.db_instance.add_entry('bands', {'name': 'first_test'})
            # print(db_instance.display_table(table_name='bands', return_json=False))
            result = self.db_instance.update_entry(
                'bands', {'id': 1, 'name': 'second_test'})
            result_no_table = self.db_instance.update_entry(
                'wrong_table', {'id': 1, 'name': 'third_test'})
            result_no_id = self.db_instance.update_entry(
                'bands', {'name': 'fourth_test'})
            result_no_entry = self.db_instance.update_entry(
                'bands', {'id': 100, 'name': 'fifth_test'})

            self.assertEqual(result, "Updated entry in table: bands")
            self.assertEqual(
                result_no_table, "Table (wrong_table) does not exist.")
            self.assertEqual(result_no_id, "id column is missing")
            # self.assertEqual(result_no_entry, "There is no such entry!!")

    # def test_delete_by_id(self):
    #     with patch('db_operations.Database') as mock_db_class:


if __name__ == '__main__':
    unittest.main()
