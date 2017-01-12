import os
import unittest
import pocketcasts

USERNAME = os.environ.get('POCKETCAST_USER')
PASSWORD = os.environ.get('POCKETCAST_PASSWORD')

class PocketcastTest(unittest.TestCase):
    pocket = pocketcasts.Pocketcasts(USERNAME, PASSWORD)

    def test_get_top_charts(self):
        response = self.pocket.get_top_charts()

    def test_get_featured(self):
        response = self.pocket.get_featured()

    def test_get_trending(self):
        response = self.pocket.get_trending()

if __name__ == '__main__':
    unittest.main()
