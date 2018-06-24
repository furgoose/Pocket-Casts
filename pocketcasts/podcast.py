class Podcast(object):
    """Class for podcast information and methods"""
    class SortOrder(object):
        """Class to allow ease of reference to sort orders"""
        NewestToOldest = 3
        OldestToNewest = 2

    def __init__(self, api, **kwargs):
        """

        Args:
            api (pocketcasts.Pocketcasts): The API object
            **kwargs: Other information about the podcast
        """
        self._api = api

        self._uuid = kwargs.get('uuid', '')
        self._title = kwargs.get('title', '')
        self._author = kwargs.get('author', '')
        self._description = kwargs.get('description', '')
        self._feed = kwargs.get('feed', '')
        self._itunes = kwargs.get('itunes', '')
        self._website = kwargs.get('website', '')

        self._episodes_sort_order = kwargs.get('episodes_sort_order', Podcast.SortOrder.NewestToOldest)

        self._language = kwargs.get('language', '')
        self._categories = str(kwargs.get('category', '')).split('\n')

        self._thumbnail_url_src = kwargs.get('thumbnail_url', '')
        self._thumbnail_url_small = "http://static.pocketcasts.com/discover/images/130/{}.jpg".format(self.uuid)
        self._thumbnail_url_medium = "http://static.pocketcasts.com/discover/images/200/{}.jpg".format(self.uuid)
        self._thumbnail_url_large = "http://static.pocketcasts.com/discover/images/280/{}.jpg".format(self.uuid)
        self._media_type = kwargs.get('media_type', '')

    def __repr__(self):
        return f"{self.__class__} ({self.title})"

    @property
    def api(self):
        """Get the API object"""
        return self._api

    @property
    def uuid(self):
        """Get the podcast UUID"""
        return self._uuid

    @property
    def title(self):
        """Get the podcast title"""
        return self._title

    @property
    def author(self):
        """Get the podcast author"""
        return self._author

    @property
    def description(self):
        """Get the podcast description"""
        return self._description

    @property
    def website(self):
        """Get the podcast website URL"""
        return self._website

    @property
    def sort_order(self):
        """Get the podcast sort order"""
        return self._episodes_sort_order

    @property
    def language(self):
        """Get the podcast language"""
        return self._language

    @property
    def categories(self):
        """Get the podcast categories"""
        return self._categories

    @property
    def thumbnail_url_src(self):
        """Get the source podcast image"""
        return self._thumbnail_url_src

    @property
    def thumbnail_url_small(self):
        """Get the small podcast image (130x130)"""
        return self._thumbnail_url_small

    @property
    def thumbnail_url_medium(self):
        """Get the medium podcast image (200x200)"""
        return self._thumbnail_url_medium

    @property
    def thumbnail_url_large(self):
        """Get the large podcast image (280x280)"""
        return self._thumbnail_url_large

    @property
    def subscribed(self):
        """Get and set the subscribed status of the podcast"""
        podcasts = self._api.get_subscribed_podcasts()
        for x in podcasts:
            if x.uuid == self.uuid:
                return True
        return False

    @subscribed.setter
    def subscribed(self, status):
        if status:
            self._api.subscribe_podcast(self)
        else:
            self._api.unsubscribe_podcast(self)
