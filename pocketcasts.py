import requests


class Pocketcasts(object):
    def __init__(self, email, password=None):
        self.username = email
        self.password = password

        self.session = requests.Session()
        if password:
            self._login()

    def _make_req(self, url, data=None):
        if data:
            req = requests.Request('POST', url, data=data, cookies=self.session.cookies)
        else:
            req = requests.Request('GET', url, cookies=self.session.cookies)
        prepped = req.prepare()
        return self.session.send(prepped)

    def _login(self):
        """
        Authenticate using "https://play.pocketcasts.com/users/sign_in"
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
        page = self._make_req("https://static.pocketcasts.com/discover/json/popular_world.json").json()
        if page['status'] != 'ok':
            raise Exception('Getting top charts failed')
        return page['result']['podcasts']

    def get_featured(self):
        page = self._make_req("https://static.pocketcasts.com/discover/json/featured.json").json()
        if page['status'] != 'ok':
            raise Exception('Getting featured podcasts failed')
        return page['result']['podcasts']

    def get_trending(self):
        page = self._make_req("https://static.pocketcasts.com/discover/json/trending.json").json()
        if page['status'] != 'ok':
            raise Exception('Getting trending podcasts failed')
        return page['result']['podcasts']

    def get_episode_info(self, uuid, episode_uuid):
        data = {
            'uuid': uuid,
            'episode_uuid': episode_uuid
        }
        return self._make_req("https://play.pocketcasts.com/web/podcasts/podcast.json", data=data).json()['episode']

    def get_podcast_info(self, uuid):
        data = {
            'uuid': uuid
        }

    def get_episode_notes(self, uuid):
        data = {
            'uuid': uuid
        }
        return self._make_req("https://play.pocketcasts.com/web/episodes/show_notes.json", data=data)\
            .json()['show_notes']