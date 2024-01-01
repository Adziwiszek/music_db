import unittest
from unittest.mock import MagicMock, patch
import sys
# setting path
sys.path.append('../music_db')
from db_operations import *

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Create a mock engine and session for testing
        self.mock_engine = MagicMock()
        self.mock_session = MagicMock()

    def test_add_entry(self):
        # Create an instance of your database class with the mock engine and session
        db_instance = Database()
        db_instance.engine = self.mock_engine
        db_instance.session = self.mock_session

        with patch('db_operations.Band') as mock_band_class:
            result = db_instance.add_entry('bands', {'name': 'Test Band'})
            result_no_table = db_instance.add_entry('wrong_table', {'name': 'Test Band'})
            result_wrong_column = db_instance.add_entry('bands', {'wrong_col': 'Test Band'})
            
            self.assertEqual(result_no_table, "Table (wrong_table) does not exist.")
            self.assertEqual(result_wrong_column, "Can't add the entry to the database, there's no column wrong_col in table bands")
            self.assertEqual(result, "Added entry to the (bands) table.")

    def test_update_entry(self):
        # Create an instance of your database class with the mock engine and session
        db_instance = Database()
        db_instance.engine = self.mock_engine
        db_instance.session = self.mock_session

        with patch('db_operations.Band') as mock_band_class:
            db_instance.add_entry('bands', {'name': 'first_test'})
            result = db_instance.update_entry('bands', {'id': 1, 'name':'second_test'})
            self.assertEqual(result, "Updated entry in table: bands")
            

    
if __name__ == '__main__':
    unittest.main()