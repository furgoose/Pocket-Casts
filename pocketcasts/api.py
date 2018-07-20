"""Unofficial API for pocketcasts.com"""
from requests import request
from .podcast import _Podcast
from .episode import _Episode
from .network import _Network

__version__ = "0.2.3"
__author__ = "Fergus Longley"
__url__ = "https://github.com/furgoose/Pocket-Casts"

def require_login(function):
        def wrapper(self, *args, **kwargs):
            if not self._logged_in:
                raise Exception("You must be logged in to use this function")
            else:
                function(self, *args, **kwargs)
        return wrapper


class Pocketcasts(object):
    """The main class for making getting and setting information from the server"""
    class Podcast:
        instances = {}
        def __new__(self, api, uuid, episodes=[], **kwargs):
            if uuid not in Pocketcasts.Podcast.instances:
                Pocketcasts.Podcast.instances[uuid] = _Podcast(api, uuid, episodes=episodes, **kwargs)
            else:
                Pocketcasts.Podcast.instances[uuid]._update(episodes, **kwargs)
            return Pocketcasts.Podcast.instances[uuid]

    class Episode:
        instances = {}
        def __new__(self, api, uuid, podcast=None, **kwargs):
            if uuid not in Pocketcasts.Episode.instances:
                Pocketcasts.Episode.instances[uuid] = _Episode(api, uuid, podcast=podcast, **kwargs)
            else:
                Pocketcasts.Episode.instances[uuid]._update(**kwargs)
            return Pocketcasts.Episode.instances[uuid]

    class Network:
        instances = {}
        def __new__(self, id, **kwargs):
            if id not in Pocketcasts.Network.instances:
                Pocketcasts.Network.instances[id] = _Network(id, **kwargs)
            else:
                Pocketcasts.Network.instances[id]._update(**kwargs)
            return Pocketcasts.Network.instances[id]
        

    def __init__(self):
        """

        Args:
            email (str): email of user
            password (str): password of user
        """
        self._logged_in = False
        self._token = ""

    def login(self, username, password):
        """Authenticate using "https://api.pocketcasts.com/user/login"

        Returns:
            bool: True is successful

        Raises:
            Exception: If login fails

        :return: 
        """
        login_url = "https://api.pocketcasts.com/user/login"
        data = f'{{"email":"{username}","password":"{password}","scope":"webplayer"}}'
        headers = {"origin": "https://playbeta.pocketcasts.com"}
        response = request("POST", login_url, data=data, headers=headers).json()

        if "message" in response:
            raise Exception("Login Failed")
        else:
            self._token = response['token']
            self._logged_in = True
            return True

    @require_login
    def _post_with_auth(self, url, data):
        headers = {
            'authorization': f'Bearer {self._token}',
            'origin': "https://playbeta.pocketcasts.com"
        }
        attempt = request("POST", url, data=data, headers=headers)
        if not attempt.ok:
            raise Exception("Invalid request") 
        return attempt

    def _create_list_episodes(self, episode_list):
        results = []
        for episode in episode_list:
            if 'podcast' in episode:
                pod = episode.pop('podcast')
                if type(pod) == dict:
                    podcast = self.Podcast(self, pod['uuid'], **{'title': pod['title']})
                else:
                    podcast = self.Podcast(self, pod)
            else:
                podcast = self.Podcast(self, episode['podcastUuid'], **{'title': episode.get('podcastTitle')})
            results.append(self.Episode(self, episode.pop('uuid'), podcast=podcast, **episode))
        return results

    def _create_list_podcasts(self, podcast_list):
        results = []
        for podcast in podcast_list:
            results.append(self.Podcast(self, podcast.pop('uuid'), **podcast))
        return results

    def get_top(self):
        """Get the top podcasts

        Returns:
            list: A list of the top 100 podcasts as Podcast objects

        """
        attempt = request("GET", "https://static2.pocketcasts.com/share/list/popular.json").json()
        return self._create_list_podcasts(attempt['podcasts'])

    def get_featured(self):
        """Get the featured podcasts

        Returns:
            list: A list of the 30 featured podcasts as Podcast objects

        """
        attempt = request("GET", "https://static2.pocketcasts.com/share/list/featured.json").json()
        return self._create_list_podcasts(attempt['podcasts'])

    def get_trending_podcasts(self):
        """Get the trending podcasts

        Returns:
            list: A list of the 100 trending podcasts as Podcast objects

        """
        attempt = request("GET", "https://static2.pocketcasts.com/share/list/trending.json").json()
        return self._create_list_podcasts(attempt['podcasts'])

    def get_trending_episodes(self):
        attempt = request('GET', "https://static2.pocketcasts.com/discover/json/trending-episodes.json").json()
        return self._create_list_episodes(attempt['result']['episodes'])

    def get_new(self):
        attempt = request("GET", "https://static2.pocketcasts.com/share/list/new-podcasts.json").json()
        return self._create_list_podcasts(attempt['podcasts'])

    def get_discover(self):
        attempt = request("GET", "https://static2.pocketcasts.com/share/list/web-discover-list.json").json()
        return (attempt['title'], self._create_list_podcasts(attempt['podcasts']))

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
        page = self._post_with_auth('https://api.pocketcasts.com/user/episode', data)
        page = page.json()
        podcast = self.Podcast(self, page['podcastUuid'], **{'title': page.get('podcastTitle')})
        return self.Episode(self, page.pop('uuid'), podcast=podcast, **page)

    @require_login
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

    @require_login
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
        attempt = self._post_with_auth('https://api.pocketcasts.com/user/podcast/list', {})
        return self._create_list_podcasts(attempt.json()['podcasts'])

    def get_new_releases(self):
        """Get newly released podcasts from a user's subscriptions

        Returns:
            List[pocketcasts.episode.Episode]: A list of episodes
        """
        attempt = self._post_with_auth('https://api.pocketcasts.com/user/new_releases', {}).json()
        if len(attempt) != 0:
            return self._create_list_episodes(attempt['episodes'])
        return []

    def get_in_progress(self):
        """Get all in progress episodes

        Returns:
            List[pocketcasts.episode.Episode]: A list of episodes

        """
        attempt = self._post_with_auth('https://api.pocketcasts.com/user/in_progress', {}).json()
        if len(attempt) != 0:
            return self._create_list_episodes(attempt['episodes'])
        return []

    def get_starred(self):
        """Get all starred episodes

        Returns:
            List[pocketcasts.episode.Episode]: A list of episodes
        """
        attempt = self._post_with_auth('https://api.pocketcasts.com/user/starred', {}).json()
        if len(attempt) != 0:
            return self._create_list_episodes(attempt['episodes'])
        return []

    def update_starred(self, pod_uuid, epi_uuid, starred):
        """Star or unstar an episode

        Args:
            pod_uuid (str): A podcast uuid
            epi_uuid (str): An episode uuid
            starred (bool): Starred status
        """
        headers = {
            'authorization': f'Bearer {self._token}',
            'origin': "https://playbeta.pocketcasts.com"
        }
        data = f'{{"uuid":"{epi_uuid}","podcast":"{pod_uuid}","star":{"true" if starred else "false"}}}'
        request("POST", "https://api.pocketcasts.com/sync/update_episode_star", data=data, headers=headers)

    def queue_play_now(self, pod_uuid, epi_uuid):
        data = f'{{"episode":{{"uuid":"{epi_uuid}","podcast":"{pod_uuid}"}}}}'
        self._post_with_auth("https://api.pocketcasts.com/up_next/play_now", data)

    def queue_play_next(self, pod_uuid, epi_uuid):
        data = f'{{"episode":{{"uuid":"{epi_uuid}","podcast":"{pod_uuid}"}}}}'
        self._post_with_auth("https://api.pocketcasts.com/up_next/play_next", data)

    def get_queue(self):
        data = '{"version":2}'
        page = self._post_with_auth("https://api.pocketcasts.com/up_next/list", data)
        return self._create_list_episodes(page.json()['episodes'])

    def subscribe_podcast(self, podcast_uuid):
        data = f'{{"uuid":{podcast_uuid}}}'
        self._post_with_auth('https://api.pocketcasts.com/user/podcast/subscribe', data)

    def unsubscribe_podcast(self, podcast_uuid):
        data = f'{{"uuid":{podcast_uuid}}}'
        self._post_with_auth('https://api.pocketcasts.com/user/podcast/unsubscribe', data)

    def search_podcasts(self, search_str):
        data = f'{{"term":"{search_str}"}}'
        page = self._post_with_auth('https://api.pocketcasts.com/discover/search', data)
        return self._create_list_podcasts(page.json()['podcasts'])
