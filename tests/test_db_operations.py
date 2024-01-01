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

    def test_add_entry_success(self):
        # Create an instance of your database class with the mock engine and session
        db_instance = Database()
        db_instance.engine = self.mock_engine
        db_instance.session = self.mock_session

        with patch('db_operations.Band') as mock_band_class:
            #mock_band_instance = MagicMock()
            #mock_band_instance.id = 1
            #mock_band_class.query.filter_by.return_value.first.return_value = mock_band_instance
            
            #self.mock_session.execute.return_value = MagicMock()
            #self.mock_session.commit.return_value = MagicMock()

            result = db_instance.add_entry('bands', {'name': 'Test Band'})

            self.assertEqual(result, "Added entry to the (bands) table.")

            #self.mock_session.execute.assert_called_once()
            #self.mock_session.commit.assert_called_once()

    def test_add_entry_failure(self):
        # Create an instance of your database class with the mock engine and session
        db_instance = Database()
        db_instance.engine = self.mock_engine
        db_instance.session = self.mock_session

        with patch('db_operations.Band') as mock_band_class:
            result_no_table = db_instance.add_entry('wrong_table', {'name': 'Test Band'})
            result_wrong_column = db_instance.add_entry('bands', {'wrong_col': 'Test Band'})
            
            self.assertEqual(result_no_table, "Table (wrong_table) does not exist.")
            self.assertEqual(result_wrong_column, "Can't add the entry to the database, there's no column wrong_col in table bands")

if __name__ == '__main__':
    unittest.main()