from datetime import datetime
from enum import Enum
from .podcast import _Podcast as Podcast

def format_time(time_string):
    for format in ('%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%d %H:%M:%S'):
        try:
            return datetime.strptime(time_string, format)
        except ValueError:
            pass
    raise ValueError(f"No format found for {time_string}")

class _Episode(object):
    """Class for podcast episodes"""
    class PlayingStatus(Enum):
        """Class to allow ease of reference to play statuses"""
        Playing = 1
        Unplayed = 2
        Played = 3

    def __init__(self, api, uuid, podcast=None, **kwargs):
        """

        Args:
            api: Api object
            **kwargs: Other information about episode
        """
        self._api = api
        self._podcast = podcast
        self._uuid = uuid

        self._update(**kwargs)
        
    def _update(self, **kwargs):
        self._title = kwargs.get('title')
        self._duration = kwargs.get('duration')
        self._file_size = kwargs.get('file_size')
        self._file_type = kwargs.get('file_type')
        self._type = kwargs.get('type')
   
        self._url = kwargs.get('url')

        self._published = kwargs.get('published')
        self._published = format_time(self._published) if self._published is not None else None    
        
        self._starred = kwargs.get('starred')
        self._starred = bool(self._starred) if self._starred is not None else None

        self._playing_status = kwargs.get('playingStatus')
        self._playing_status = self.PlayingStatus(self._playing_status) if self._playing_status is not None else self.PlayingStatus.Unplayed

        self._played_up_to = kwargs.get('played_up_to')

    def __repr__(self):
        return f"{self.__class__} at {hex(id(self))} ({self._title})"
