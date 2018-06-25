from datetime import datetime
from enum import Enum

class _Podcast(object):
    """Class for podcast information and methods"""
    class SortOrder(Enum):
        """Class to allow ease of reference to sort orders"""
        NewestToOldest = 3
        OldestToNewest = 2

    def __init__(self, api, uuid, episodes=[], **kwargs):
        """

        Args:
            api (pocketcasts.Pocketcasts): The API object
            episodes: List of episode objects
            **kwargs: Other information about the podcast
        """
        self._api = api
        self._uuid = uuid
        
        self.update(episodes, **kwargs)

    def update(self, episodes, **kwargs):
        self._title = kwargs.get('title')
        self._author = kwargs.get('author')
        self._description = kwargs.get('description')
        self._feed = kwargs.get('feed')
        self._itunes = kwargs.get('itunes')

        self._website = kwargs.get('website')
        self._website = kwargs.get('url', self._website)

        self._categories = kwargs.get('category')
        self._categories = str(self._categories).split('\n') if self._categories is not None else None

        self._audio = kwargs.get('audio')
        self._audio = bool(self._audio) if self._audio is not None else None

        self._show_type = kwargs.get('show_type')

        self._episode_frequency = kwargs.get('episode_frequency')

        self._estimated_next_episode_at = kwargs.get('estimated_next_episode_at')
        self._estimated_next_episode_at = (datetime.strptime(self._estimated_next_episode_at, '%Y-%m-%dT%H:%M:%SZ') 
                                            if self._estimated_next_episode_at is not None else None)
        
        self._has_seasons = kwargs.get('has_seasons')
        self._has_seasons = bool(self._has_seasons) if self._has_seasons is not None else None

        self._season_count = kwargs.get('season_count')
        self._episode_count = kwargs.get('episode_count')

        self._has_more_episodes = kwargs.get('has_more_episodes')
        self._has_more_episodes = bool(self._has_more_episodes) if self._has_more_episodes is not None else None

        self._episodes = episodes

        self._episodes_sort_order = kwargs.get('episodesSortOrder')
        self._episodes_sort_order = self.SortOrder(self._episodes_sort_order) if self._episodes_sort_order is not None else self.SortOrder.NewestToOldest

        self._unplayed = kwargs.get('unplayed')
        self._unplayed = bool(self._unplayed) if self._unplayed is not None else None

    def __repr__(self):
        return f"{self.__class__} at {hex(id(self))} ({self._title})"
