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

        # Mock the Band class for the 'band_name' check
        with patch('db_operations.Band') as mock_band_class:
            # Mock the query method to return a Band instance
            mock_band_instance = MagicMock()
            mock_band_instance.id = 1
            mock_band_class.query.filter_by.return_value.first.return_value = mock_band_instance

            # Mock the execute method to avoid database interactions
            self.mock_session.execute.return_value = MagicMock()

            # Mock the commit method to avoid actual commits
            self.mock_session.commit.return_value = MagicMock()

            # Call the add_entry method
            result = db_instance.add_entry('bands', {'band_name': 'Test Band'})

            # Assert the expected outcome
            self.assertEqual(result, "Added entry to the (bands) table.")

            # Assert that the execute method was called
            self.mock_session.execute.assert_called_once()

            # Assert that the commit method was called
            self.mock_session.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()