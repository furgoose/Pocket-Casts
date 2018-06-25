"""Unofficial API for pocketcasts.com"""
import requests
from requests import request
from .podcast import _Podcast
from .episode import _Episode
from .network import _Network

__version__ = "0.2.3"
__author__ = "Fergus Longley"
__url__ = "https://github.com/furgoose/Pocket-Casts"


class Pocketcasts(object):
    """The main class for making getting and setting information from the server"""
    class Podcast:
        instances = {}
        def __new__(self, api, uuid, episodes=[], **kwargs):
            if uuid not in Pocketcasts.Podcast.instances:
                Pocketcasts.Podcast.instances[uuid] = _Podcast(api, uuid, episodes=episodes, **kwargs)
            else:
                Pocketcasts.Podcast.instances[uuid].update(episodes, **kwargs)
            return Pocketcasts.Podcast.instances[uuid]

    class Episode:
        instances = {}
        def __new__(self, api, uuid, podcast=None, **kwargs):
            if uuid not in Pocketcasts.Episode.instances:
                Pocketcasts.Episode.instances[uuid] = _Episode(api, uuid, podcast=podcast, **kwargs)
            else:
                Pocketcasts.Episode.instances[uuid].update(**kwargs)
            return Pocketcasts.Episode.instances[uuid]

    class Network:
        instances = {}
        def __new__(self, id, **kwargs):
            if id not in Pocketcasts.Network.instances:
                Pocketcasts.Network.instances[id] = _Network(id, **kwargs)
            else:
                Pocketcasts.Network.instances[id].update(**kwargs)
            return Pocketcasts.Network.instances[id]
        

    def __init__(self, email, password):
        """

        Args:
            email (str): email of user
            password (str): password of user
        """
        self._username = email
        self._password = password
        self._token = ""

        self._session = requests.Session()
        self._login()

    def _login(self):
        """Authenticate using "https://api.pocketcasts.com/user/login"

        Returns:
            bool: True is successful

        Raises:
            Exception: If login fails

        :return: 
        """
        login_url = "https://api.pocketcasts.com/user/login"
        data = f'{{"email":"{self._username}","password":"{self._password}","scope":"webplayer"}}'
        headers = {"origin": "https://playbeta.pocketcasts.com"}
        response = request("POST", login_url, data=data, headers=headers).json()

        if "message" in response:
            raise Exception("Login Failed")
        else:
            self._token = response['token']
            return True

    def _create_list_from_url(self, url):
        page = request("GET", url).json()
        results = []
        for podcast in page['podcasts']:
            results.append(self.Podcast(self, page['uuid'], **podcast))
        return results

    def get_top(self):
        """Get the top podcasts

        Returns:
            list: A list of the top 100 podcasts as Podcast objects

        """
        return self._create_list_from_url("https://static2.pocketcasts.com/share/list/popular.json")

    def get_featured(self):
        """Get the featured podcasts

        Returns:
            list: A list of the 30 featured podcasts as Podcast objects

        """
        return self._create_list_from_url("https://static2.pocketcasts.com/share/list/featured.json")

    def get_trending_podcasts(self):
        """Get the trending podcasts

        Returns:
            list: A list of the 100 trending podcasts as Podcast objects

        """
        return self._create_list_from_url("https://static2.pocketcasts.com/share/list/trending.json")

    def get_trending_episodes(self):
        page = request('GET', "https://static2.pocketcasts.com/discover/json/trending-episodes.json").json()
        results = []
        for episode in page['result']['episodes']:
            results.append(self.Episode(self, episode.pop('uuid'), **episode))
        return results

    def get_new(self):
        return self._create_list_from_url("https://static2.pocketcasts.com/share/list/new-podcasts.json")

    def get_discover(self):
        url = "https://static2.pocketcasts.com/share/list/web-discover-list.json"
        page = request("GET", url).json()
        return (page['title'], self._create_list_from_url(url))

    def get_networks(self):
        page = request("GET", "https://static2.pocketcasts.com/discover/json/network_list.json").json()
        results = []
        for network in page['result']['networks']:
            results.append(self.Network(network.pop('id'), **network))
        return results

    def get_episode(self, uuid):
        """Returns an episode object corresponding to the uuid provided

        Args:
            e_uuid (str): The episode UUID

        Returns:
            class: An Episode class with all information about an episode

        """
        data = f'{{"uuid":"{uuid}"}}'
        headers = {
            'authorization': f'Bearer {self._token}',
            'origin': "https://playbeta.pocketcasts.com"
        }
        page = request('POST', 'https://api.pocketcasts.com/user/episode', data=data, headers=headers)
        if not page.ok:
            raise Exception("Invalid UUID")
        page = page.json()
        podcast = self.Podcast(self, page['podcastUuid'], **{'title': page.get('podcastTitle')})
        return self.Episode(self, page.pop('uuid'), podcast=podcast, **page)

    def get_podcast(self, uuid):
        """Get a podcast from it's UUID

        Args:
            uuid (str): The UUID of the podcast

        Returns:
            pocketcasts.Podcast: A podcast object corresponding to the UUID provided.

        """
        headers = {
            'authorization': f'Bearer {self._token}'
        }
        page = request('GET', f'https://cache.pocketcasts.com/podcast/full/{uuid}/0/3/1000', headers=headers).json()
        podcast_dict = page.pop('podcast')
        episode_dict = podcast_dict.pop('episodes')
        podcast = self.Podcast(self, podcast_dict.pop('uuid'), **{**page, **podcast_dict})
        episodes = [self.Episode(self, x.pop('uuid'), podcast=podcast, **x) for x in episode_dict]
        podcast._episodes = episodes
        return podcast

    def get_episode_notes(self, episode_uuid):
        """Get the notes for an episode

        Args:
            episode_uuid (str): The episode UUID

        Returns:
            str: The notes for the episode UUID provided

        """
        headers = {
            'authorization': f'Bearer {self._token}'
        }
        return request("GET", f"https://cache.pocketcasts.com/episode/show_notes/{episode_uuid}", headers=headers).json()['show_notes']

    def get_subscribed_podcasts(self):
        """Get the user's subscribed podcasts

        Returns:
            List[pocketcasts.podcast.Podcast]: A list of podcasts

        """
        headers = {
            'authorization': f'Bearer {self._token}',
            'origin': "https://playbeta.pocketcasts.com"
        }
        attempt = request("POST", 'https://api.pocketcasts.com/user/podcast/list', headers=headers).json()
        results = []
        for podcast in attempt['podcasts']:
            results.append(self.Podcast(self, podcast.pop('uuid'), **podcast))
        return results

    def _create_list_episodes(self, url):
        headers = {
            'authorization': f'Bearer {self._token}',
            'origin': "https://playbeta.pocketcasts.com"
        }
        attempt = request("POST", url, headers=headers).json()
        results = []
        for episode in attempt['episodes']:
            podcast = self.Podcast(self, episode['podcastUuid'], **{'title': episode.get('podcastTitle')})
            results.append(self.Episode(self, episode.pop('uuid'), podcast=podcast, **episode))
        return results

    def get_new_releases(self):
        """Get newly released podcasts from a user's subscriptions

        Returns:
            List[pocketcasts.episode.Episode]: A list of episodes
        """
        return self._create_list_episodes('https://api.pocketcasts.com/user/new_releases')

    def get_in_progress(self):
        """Get all in progress episodes

        Returns:
            List[pocketcasts.episode.Episode]: A list of episodes

        """
        return self._create_list_episodes('https://api.pocketcasts.com/user/in_progress')

    def get_starred(self):
        """Get all starred episodes

        Returns:
            List[pocketcasts.episode.Episode]: A list of episodes
        """
        return self._create_list_episodes('https://api.pocketcasts.com/user/starred')

    def update_starred(self, pod_uuid, epi_uuid, starred):
        """Star or unstar an episode

        Args:
            pod_uuid (str): A podcast class
            epi_uuid (str): An episode class to be updated
            starred (bool): Starred status
        """
        headers = {
            'authorization': f'Bearer {self._token}',
            'origin': "https://playbeta.pocketcasts.com"
        }
        data = f'{{"uuid":"{epi_uuid}","podcast":"{pod_uuid}","star":{"true" if starred else "false"}}}'
        request("POST", "https://api.pocketcasts.com/sync/update_episode_star", data=data, headers=headers)

    def update_playing_status(self, pod_uuid, epi_uuid, status=_Episode.PlayingStatus.Unplayed):
        pass

    def update_played_position(self, podcast, episode, position):
        pass

    def subscribe_podcast(self, podcast):
        pass

    def unsubscribe_podcast(self, podcast):
        pass

    def search_podcasts(self, search_str):
        pass
