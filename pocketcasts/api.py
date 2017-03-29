"""Unofficial API for pocketcasts.com"""
import requests
from .podcast import Podcast
from .episode import Episode

__version__ = "0.2.3"
__author__ = "Fergus Longley"
__url__ = "https://github.com/exofudge/Pocket-Casts"


class Pocketcasts(object):
    def __init__(self, email, password):
        self.username = email
        self.password = password

        self.session = requests.Session()
        self._login()

    def _make_req(self, url, method='GET', data=None):
        """Makes a HTTP GET/POST request

        :param url: A string, the url to make a request to
        :param method: A string, The method to use. Defaults to 'GET'
        :param data: A dict, data to send with a POST request. Defaults to None.
        :return: A :class:`response.models.Response`
        """
        if method == 'JSON':
            req = requests.Request('POST', url, json=data, cookies=self.session.cookies)
        elif method == 'POST' or data:
            req = requests.Request('POST', url, data=data, cookies=self.session.cookies)
        elif method == 'GET':
            req = requests.Request('GET', url, cookies=self.session.cookies)
        else:
            raise Exception("Invalid method")
        prepped = req.prepare()
        return self.session.send(prepped)

    def _login(self):
        """Authenticate using "https://play.pocketcasts.com/users/sign_in"

        Returns:
            bool: True is successful

        Raises:
            Exception: If login fails

        """
        login_url = "https://play.pocketcasts.com/users/sign_in"
        data = {"[user]email": self.username, "[user]password": self.password}
        attempt = self._make_req(login_url, data=data)

        # TODO Find a more robust way to check if login failed
        if "Invalid email or password" in attempt.text:
            raise Exception("Login Failed")
        else:
            return True

    def get_top_charts(self):
        """Get the top podcasts

        Returns:
            list: A list of the top 100 podcasts as Podcast objects

        Raises:
            Exception: If the top charts cannot be obtained

        """
        page = self._make_req("https://static.pocketcasts.com/discover/json/popular_world.json").json()
        results = []
        for podcast in page['result']['podcasts']:
            uuid = podcast.pop('uuid')
            results.append(Podcast(uuid, self, **podcast))
        return results

    def get_featured(self):
        """Get the featured podcasts

        Returns:
            list: A list of the 30 featured podcasts as Podcast objects

        Raises:
            Exception: If the featured podcasts cannot be obtained

        """
        page = self._make_req("https://static.pocketcasts.com/discover/json/featured.json").json()
        results = []
        for podcast in page['result']['podcasts']:
            uuid = podcast.pop('uuid')
            results.append(Podcast(uuid, self, **podcast))
        return results

    def get_trending(self):
        """Get the trending podcasts

        Returns:
            list: A list of the 100 trending podcasts as Podcast objects

        Raises:
            Exception: If the trending podcasts cannot be obtained

        """
        page = self._make_req("https://static.pocketcasts.com/discover/json/trending.json").json()
        results = []
        for podcast in page['result']['podcasts']:
            uuid = podcast.pop('uuid')
            results.append(Podcast(uuid, self, **podcast))
        return results

    def get_episode(self, pod, e_uuid):
        # TODO figure out what id is/does
        """Returns an episode object corresponding to the uuid's provided

        Args:
            pod (class): The podcast class
            e_uuid (str): The episode UUID

        Returns:
            class: An Episode class with all information about an episode

        Examples:
            >>> p = Pocketcasts(email='email@email.com')
            >>> pod = p.get_podcast('12012c20-0423-012e-f9a0-00163e1b201c')
            >>> p.get_episode(pod, 'a35748e0-bb4d-0134-10a8-25324e2a541d')
            <class 'episode.Episode'> ({
            '_size': 10465287,
            '_is_video': False,
            '_url': 'http://.../2017-01-12-sysk-watersheds.mp3?awCollectionId=1003&awEpisodeId=923109',
            '_id': None,
            '_duration': '1934',
            '_is_deleted': '',
            '_title': 'How Watersheds Work',
            '_file_type': 'audio/mpeg',
            '_played_up_to': 1731,
            '_published_at': '2017-01-12 08:00:00',
            '_podcast': <class 'podcast.Podcast'> (...),
            '_playing_status': 2,
            '_starred': False,
            '_uuid': 'a35748e0-bb4d-0134-10a8-25324e2a541d'})

        """
        data = {
            'uuid': pod.uuid,
            'episode_uuid': e_uuid
        }
        attempt = self._make_req('https://play.pocketcasts.com/web/podcasts/podcast.json', data=data).json()['episode']
        attempt.pop('uuid')
        episode = Episode(e_uuid, pod, **attempt)
        return episode

    def get_podcast(self, uuid):
        data = {
            'uuid': uuid
        }
        attempt = self._make_req('https://play.pocketcasts.com/web/podcasts/podcast.json', data=data).json()['podcast']
        attempt.pop('uuid')
        podcast = Podcast(uuid, self, **attempt)
        return podcast

    def get_podcast_episodes(self, pod, sort=Podcast.SortOrder.NewestToOldest):
        """Get all episodes of a podcasts

        Args:
            pod (class): The podcast class
            sort (int): The sort order, 3 for Newest to oldest, 2 for Oldest to newest

        Returns:
            list: A list of Episode classes

        Examples:
            >>> p = Pocketcasts('email@email.com')
            >>> pod = p.get_podcast('12012c20-0423-012e-f9a0-00163e1b201c')
            >>> p.get_podcast_episodes(pod)
            [<class 'episode.Episode'> ({
            '_size': 17829778,
            '_is_video': False,
            '_url': 'http://.../2017-02-21-sysk-death-tax-final.mp3?awCollectionId=1003&awEpisodeId=923250',
            '_id': None,
            '_duration': '3161',
            '_is_deleted': 0,
            '_title': 'The ins and outs of the DEATH TAX',
            '_file_type': 'audio/mpeg',
            '_played_up_to': 0,
            '_published_at': '2017-02-21 08:00:00',
            '_podcast': <class 'podcast.Podcast'> (...),
            '_playing_status': 0,
            '_starred': False,
            '_uuid': '9189eba0-da79-0134-ebdd-4114446340cb'}),
             ...]

        """
        page = 1
        more_pages = True
        episodes = []
        while more_pages:
            data = {
                'uuid': pod.uuid,
                'page': page,
                'sort': sort
            }
            attempt = self._make_req('https://play.pocketcasts.com/web/episodes/find_by_podcast.json', data=data).json()
            for epi in attempt['result']['episodes']:
                uuid = epi.pop('uuid')
                episodes.append(Episode(uuid, podcast=pod, **epi))
            if attempt['result']['total'] > len(episodes):
                page += 1
            else:
                more_pages = False
        return episodes

    def get_episode_notes(self, episode_uuid):
        """

        :param episode_uuid:
        :return:
        """
        data = {
            'uuid': episode_uuid
        }
        return self._make_req('https://play.pocketcasts.com/web/episodes/show_notes.json', data=data) \
            .json()['show_notes']

    def get_subscribed_podcasts(self):
        attempt = self._make_req('https://play.pocketcasts.com/web/podcasts/all.json', method='POST').json()
        results = []
        for podcast in attempt['podcasts']:
            uuid = podcast.pop('uuid')
            results.append(Podcast(uuid, self, **podcast))
        return results

    def get_new_releases(self):
        attempt = self._make_req('https://play.pocketcasts.com/web/episodes/new_releases_episodes.json', method='POST')
        results = []
        podcasts = {}
        for episode in attempt.json()['episodes']:
            pod_uuid = episode['podcast_uuid']
            if pod_uuid not in podcasts:
                podcasts[pod_uuid] = self.get_podcast(pod_uuid)
            uuid = episode.pop('uuid')
            results.append(Episode(uuid, podcasts[pod_uuid], **episode))
        return results

    def get_in_progress(self):
        attempt = self._make_req('https://play.pocketcasts.com/web/episodes/in_progress_episodes.json', method='POST')
        results = []
        podcasts = {}
        for episode in attempt.json()['episodes']:
            pod_uuid = episode['podcast_uuid']
            if pod_uuid not in podcasts:
                podcasts[pod_uuid] = self.get_podcast(pod_uuid)
            uuid = episode.pop('uuid')
            results.append(Episode(uuid, podcasts[pod_uuid], **episode))
        return results

    def get_starred(self):
        attempt = self._make_req('https://play.pocketcasts.com/web/episodes/starred_episodes.json', method='POST')
        results = []
        podcasts = {}
        for episode in attempt.json()['episodes']:
            pod_uuid = episode['podcast_uuid']
            if pod_uuid not in podcasts:
                podcasts[pod_uuid] = self.get_podcast(pod_uuid)
            uuid = episode.pop('uuid')
            results.append(Episode(uuid, podcasts[pod_uuid], **episode))
        return results

    def update_starred(self, podcast, episode, starred):
        data = {
            'starred': starred,
            'podcast_uuid': podcast.uuid,
            'uuid': episode.uuid
        }
        self._make_req("https://play.pocketcasts.com/web/episodes/update_episode_star.json", data=data)
        # TODO Check if successful or not

    def update_playing_status(self, podcast, episode, status=Episode.PlayingStatus.Unplayed):
        if status not in [0, 2, 3]:
            raise Exception('Invalid status.')
        data = {
            'playing_status': status,
            'podcast_uuid': podcast.uuid,
            'uuid': episode.uuid
        }
        self._make_req("https://play.pocketcasts.com/web/episodes/update_episode_position.json", data=data)

    def update_played_position(self, podcast, episode, position):
        data = {
            'uuid': episode.uuid,
            'podcast_uuid': podcast.uuid,
            'playing_status': episode.playing_status,
            'duration': episode.duration,
            'played_up_to': position
        }
        attempt = self._make_req("https://play.pocketcasts.com/web/episodes/update_episode_position.json",
                                 method='JSON', data=data)
        if attempt.json()['status'] != 'ok':
            raise Exception('Sorry your update failed.')
        return True

    def subscribe_podcast(self, podcast):
        data = {
            'uuid': podcast.uuid
        }
        self._make_req("https://play.pocketcasts.com/web/podcasts/subscribe.json", data=data)

    def unsubscribe_podcast(self, podcast):
        data = {
            'uuid': podcast.uuid
        }
        self._make_req("https://play.pocketcasts.com/web/podcasts/unsubscribe.json", data=data)

    def search_podcasts(self, search_str):
        data = {
            'term': search_str
        }
        attempt = self._make_req("https://play.pocketcasts.com/web/podcasts/search.json", data=data)
        results = []
        for podcast in attempt.json()['podcasts']:
            uuid = podcast.pop('uuid')
            results.append(Podcast(uuid, self, **podcast))
        return results
