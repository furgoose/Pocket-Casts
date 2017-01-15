import requests


class Pocketcasts(object):
    def __init__(self, email, password=None):
        self.username = email
        self.password = password

        self.session = requests.Session()
        if password:
            self._login()

    def _make_req(self, url, method='GET', data=None):
        """Makes a HTTP GET/POST request

        Args:
            url (str): The url to request data from
            method (str): The method to use. Defaults to 'GET'
            data (dict): Data to send with a POST request. Defaults to None.

        Returns:
            requests.models.Response: The response to the query

        Raises:
            Exception: If an invalid method is provided

        """
        if method == 'POST' or data:
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
        if "Oops, looks like your email or password is incorrect." in attempt.text:
            raise Exception("Login Failed")
        else:
            return True

    def get_top_charts(self):
        """Get the top podcasts

        Returns:
            list: A list of the top 100 podcasts

        Raises:
            Exception: If the top charts cannot be obtained

        """
        page = self._make_req("https://static.pocketcasts.com/discover/json/popular_world.json").json()
        if page['status'] != 'ok':
            raise Exception('Getting top charts failed')
        return page['result']['podcasts']

    def get_featured(self):
        """Get the featured podcasts

        Returns:
            list: A list of the 30 featured podcasts

        Raises:
            Exception: If the featured podcasts cannot be obtained

        """
        page = self._make_req("https://static.pocketcasts.com/discover/json/featured.json").json()
        if page['status'] != 'ok':
            raise Exception('Getting featured podcasts failed')
        return page['result']['podcasts']

    def get_trending(self):
        """Get the trending podcasts

        Returns:
            list: A list of the 100 trending podcasts

        Raises:
            Exception: If the trending podcasts cannot be obtained

        """
        page = self._make_req("https://static.pocketcasts.com/discover/json/trending.json").json()
        if page['status'] != 'ok':
            raise Exception('Getting trending podcasts failed')
        return page['result']['podcasts']

    def get_episode_info(self, uuid, episode_uuid):
        # TODO figure out what id is
        """Get the episode information for a podcast

        Args:
            uuid (str): The podcast UUID
            episode_uuid (str): The episode UUID

        Returns:
            dict: a dictionary of information related to the episode, including the following keys
                duration: the duration of the episode in seconds
                file_type: The file type
                id:
                published_at: The time the episode was released at
                size: The file size in bits
                title: The title of the episode
                url: The download/streaming url
                uuid: the uuid of the episode

        Examples:
            >>> p.get_episode_info('12012c20-0423-012e-f9a0-00163e1b201c', 'a35748e0-bb4d-0134-10a8-25324e2a541d')
            {'duration': '1934',
             'file_type': 'audio/mpeg',
             'id': None,
             'published_at': '2017-01-12 08:00:00',
             'size': 10465287,
             'title': 'How Watersheds Work',
             'url': ('http://www.podtrac.com/pts/redirect.mp3/streaming.howstuffworks.com/sysk/'
                     '2017-01-12-sysk-watersheds.mp3?awCollectionId=1003&awEpisodeId=923109'),
             'uuid': 'a35748e0-bb4d-0134-10a8-25324e2a541d'}

        """
        data = {
            'uuid': uuid,
            'episode_uuid': episode_uuid
        }
        return self._make_req('https://play.pocketcasts.com/web/podcasts/podcast.json', data=data).json()['episode']

    def get_podcast_info(self, uuid, page, sort):
        data = {
            'uuid': uuid,
            'page': page,
            'sort': sort
        }
        attempt = self._make_req('https://play.pocketcasts.com/web/episodes/find_by_podcast.json', data=data)
        return attempt.json()['result']

    def get_episode_notes(self, episode_uuid):
        data = {
            'uuid': episode_uuid
        }
        return self._make_req('https://play.pocketcasts.com/web/episodes/show_notes.json', data=data)\
            .json()['show_notes']

    def get_subscribed_podcasts(self):
        return self._make_req('https://play.pocketcasts.com/web/podcasts/all.json', method='POST').json()['podcasts']

    def get_new_releases(self):
        attempt = self._make_req('https://play.pocketcasts.com/web/episodes/new_releases_episodes.json', method='POST')
        return attempt.json()['episodes']

    def get_in_progress(self):
        attempt = self._make_req('https://play.pocketcasts.com/web/episodes/in_progress_episodes.json', method='POST')
        return attempt.json()['episodes']
