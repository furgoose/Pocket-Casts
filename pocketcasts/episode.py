from datetime import datetime

class Episode(object):
    """Class for podcast episodes"""
    class PlayingStatus(object):
        """Class to allow ease of reference to play statuses"""
        Unplayed = 0
        Playing = 2
        Played = 3

    def __init__(self, uuid, podcast, **kwargs):
        """

        Args:
            uuid (str): Episode UUID
            podcast (pocketcasts.Podcast): Podcast for the episode
            **kwargs: Other information about episode
        """
        self._podcast = podcast
        self._api = podcast.api
        self._uuid = uuid
        self._id = kwargs.get('id', '')
        self._is_deleted = kwargs.get('is_deleted', '')
        self._is_video = bool(kwargs.get('is_video', ''))
        self._file_type = kwargs.get('file_type', '')
        self._size = kwargs.get('size', '')

        self._title = kwargs.get('title', '')
        self._url = kwargs.get('url', '')
        self._duration = kwargs.get('duration', '')
        self._published_at = datetime.strptime(kwargs.get('published_at', ''), '%Y-%m-%d %H:%M:%S')
        self._starred = bool(kwargs.get('starred', ''))

        self._playing_status = kwargs.get('playing_status', Episode.PlayingStatus.Unplayed)
        self._played_up_to = kwargs.get('played_up_to', '')

    def __repr__(self):
        return "%s (%r)" % (self.__class__, self.__dict__)

    @property
    def podcast(self):
        """Get the podcast object for the episode"""
        return self._podcast

    @property
    def uuid(self):
        """Get the episode UUID"""
        return self._uuid

    @property
    def id(self):
        """Get the episode ID"""
        return self._id

    @property
    def is_deleted(self):
        """Get the is_deleted property"""
        return self._is_deleted

    @property
    def is_video(self):
        """Get the is_video property"""
        return self._is_video

    @property
    def file_type(self):
        """Get the file type"""
        return self._file_type

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
    def published_at(self):
        """Get the episode publish time"""
        return self._published_at

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
