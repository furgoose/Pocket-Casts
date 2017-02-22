import os
import unittest
import pocketcasts

USERNAME = os.environ.get('POCKETCAST_USER')
PASSWORD = os.environ.get('POCKETCAST_PASSWORD')

class PocketcastTest(unittest.TestCase):
    pocket = pocketcasts.Pocketcasts(USERNAME, password=PASSWORD)

    def test_get_top_charts(self):
        response = self.pocket.get_top_charts()

    def test_get_featured(self):
        response = self.pocket.get_featured()

    def test_get_trending(self):
        response = self.pocket.get_trending()

    def test_get_podcast(self):
        response = self.pocket.get_podcast('12012c20-0423-012e-f9a0-00163e1b201c')

    def test_get_podcast_episodes(self):
        response = self.pocket.get_podcast_episodes(self.pocket.get_trending()[0])

    def test_get_episode_notes(self):
        response = self.pocket.get_episode_notes('a35748e0-bb4d-0134-10a8-25324e2a541d')

    @unittest.skipIf(not PASSWORD, "You must have valid username/password")
    def test_get_subscribed_podcasts(self):
        response = self.pocket.get_subscribed_podcasts()

    @unittest.skipIf(not PASSWORD, "You must have valid username/password")
    def test_get_new_releases(self):
        response = self.pocket.get_new_releases()

    @unittest.skipIf(not PASSWORD, "You must have valid username/password")
    def test_get_in_progress(self):
        response = self.pocket.get_in_progress()

if __name__ == '__main__':
    unittest.main()
