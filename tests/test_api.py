import os
import unittest
import pocketcasts


USERNAME = os.environ.get('POCKETCAST_USER')
PASSWORD = os.environ.get('POCKETCAST_PASSWORD')

class PocketcastTest(unittest.TestCase):
    pocket = pocketcasts.Pocketcasts(USERNAME, PASSWORD)

    def test_invalid_method(self):
        self.assertRaises(Exception, self.pocket._make_req, 'test', method='INVALID')

    def test_invalid_login(self):
        self.assertRaises(Exception, pocketcasts.Pocketcasts, 'test', 'INVALID')

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

    def test_get_episode(self):
        pod = self.pocket.get_podcast("12012c20-0423-012e-f9a0-00163e1b201c")
        self.pocket.get_episode(pod, "7b28c700-d4f1-0134-ebdd-4114446340cb")

    def test_get_starred(self):
        self.pocket.get_starred()

    def test_search_podcasts(self):
        self.pocket.search_podcasts('test')

    def test_subscribe_functions(self):
        pod = self.pocket.get_podcast("da9bb800-e230-0132-0bd1-059c869cc4eb")
        pod.subscribed = True
        pod.subscribed = False

    def test_get_episode_notes(self):
        response = self.pocket.get_episode_notes('a35748e0-bb4d-0134-10a8-25324e2a541d')

    def test_get_subscribed_podcasts(self):
        response = self.pocket.get_subscribed_podcasts()

    def test_get_new_releases(self):
        response = self.pocket.get_new_releases()

    def test_get_in_progress(self):
        response = self.pocket.get_in_progress()

    def test_update_playing_status(self):
        pod = self.pocket.get_podcast("12012c20-0423-012e-f9a0-00163e1b201c")
        epi = self.pocket.get_podcast_episodes(pod)[-1]
        epi.playing_status = 3

    def test_invalid_update_playing_status(self):
        pod = self.pocket.get_podcast("12012c20-0423-012e-f9a0-00163e1b201c")
        epi = self.pocket.get_podcast_episodes(pod)[-1]
        with self.assertRaises(Exception) as context:
            epi.playing_status = 'invalid'
            self.assertTrue('Sorry your update failed.' in context.exception)

    def test_update_played_position(self):
        pod = self.pocket.get_podcast("12012c20-0423-012e-f9a0-00163e1b201c")
        epi = self.pocket.get_podcast_episodes(pod)[-1]
        epi.played_up_to = 2

    def test_invalid_played_position(self):
        pod = self.pocket.get_podcast("12012c20-0423-012e-f9a0-00163e1b201c")
        epi = self.pocket.get_podcast_episodes(pod)[-1]
        with self.assertRaises(Exception) as context:
            epi.played_up_to = 'invalid'
            self.assertTrue('Sorry your update failed.' in context.exception)

    def test_update_starred(self):
        pod = self.pocket.get_podcast("12012c20-0423-012e-f9a0-00163e1b201c")
        epi = self.pocket.get_podcast_episodes(pod)[-1]
        epi.starred = True
        epi.starred = False

if __name__ == '__main__':
    unittest.main()
