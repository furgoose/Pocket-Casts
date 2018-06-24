from datetime import datetime
from .podcast import Podcast

class Episode(object):
    """Class for podcast episodes"""
    class PlayingStatus(object):
        """Class to allow ease of reference to play statuses"""
        Unplayed = 0
        Playing = 2
        Played = 3

    def __init__(self, api, **kwargs):
        """

        Args:
            uuid (str): Episode UUID
            podcast (pocketcasts.Podcast): Podcast for the episode
            **kwargs: Other information about episode
        """
        self._api = api

        self._uuid = kwargs.get('uuid', '')
        self._title = kwargs.get('title', '')
        self._duration = kwargs.get('duration', '')
        self._size = kwargs.get('size', '')

        self._podcast = kwargs.get('podcast', '')
        if 'podcastUuid' in kwargs:
            self._podcast = Podcast(self._api, **{'uuid': kwargs['uuid'], 'title': kwargs['title']})        
        self._url = kwargs.get('url', '')
        self._published = kwargs.get('published', '')
        if self._published != '':
            self._published = datetime.strptime(self._published, '%Y-%m-%dT%H:%M:%SZ')
        self._starred = bool(kwargs.get('starred', ''))

        self._playing_status = kwargs.get('playing_status', Episode.PlayingStatus.Unplayed)
        self._played_up_to = kwargs.get('played_up_to', '')

    def __repr__(self):
        return f"{self.__class__} ({self.title})"

    @property
    def podcast(self):
        """Get the podcast object for the episode"""
        return self._podcast

    @property
    def uuid(self):
        """Get the episode UUID"""
        return self._uuid

    @property
    def size(self):
        """Get the episode size"""
        return self._size

    @property
    def title(self):
        """Get the episode title"""
        return self._title

    @property
    def url(self):
        """Get the episode URL"""
        return self._url

    @property
    def duration(self):
        """Get the episode duration"""
        return self._duration

    @property
    def starred(self):
        """Get and set the starred status"""
        return self._starred

    @starred.setter
    def starred(self, starred):
        star = 1 if starred else 0
        self._api.update_starred(self._podcast, self, star)
        self._starred = starred

    @property
    def playing_status(self):
        """Get and set the playing status"""
        return self._playing_status

    @playing_status.setter
    def playing_status(self, status):
        self._api.update_playing_status(self._podcast, self, status)
        if status == self.PlayingStatus.Unplayed:
            self._api.update_played_position(self._podcast, self, 0)
        self._playing_status = status

    @property
    def played_up_to(self):
        """Get and set the play duration"""
        return self._played_up_to

    @played_up_to.setter
    def played_up_to(self, position):
        self._api.update_played_position(self._podcast, self, position)
        self._played_up_to = position
