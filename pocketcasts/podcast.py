class Podcast(object):
    class SortOrder(object):
        NewestToOldest = 3
        OldestToNewest = 2

    def __init__(self, uuid, api, **kwargs):
        self._api = api
        self._uuid = uuid
        self._id = kwargs.get('id', '')
        self._title = kwargs.get('title', '')
        self._author = kwargs.get('author', '')
        self._description = kwargs.get('description', '')
        self._url = kwargs.get('url', '')
        self._episodes_sort_order = kwargs.get('episodes_sort_order', Podcast.SortOrder.NewestToOldest)

        self._language = kwargs.get('language', '')
        self._categories = str(kwargs.get('category', '')).split('\n')

        self._thumbnail_url_src = kwargs.get('thumbnail_url', '')
        self._thumbnail_url_small = "http://static.pocketcasts.com/discover/images/130/{}.jpg".format(uuid)
        self._thumbnail_url_medium = "http://static.pocketcasts.com/discover/images/200/{}.jpg".format(uuid)
        self._thumbnail_url_large = "http://static.pocketcasts.com/discover/images/280/{}.jpg".format(uuid)
        self._media_type = kwargs.get('media_type', '')

    def __repr__(self):
        return "%s (%r)" % (self.__class__, self.__dict__)

    @property
    def api(self):
        return self._api

    @property
    def uuid(self):
        return self._uuid

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def description(self):
        return self._description

    @property
    def url(self):
        return self._url

    @property
    def sort_order(self):
        return self._episodes_sort_order

    @property
    def language(self):
        return self._language

    @property
    def categories(self):
        return self._categories

    @property
    def thumbnail_url_src(self):
        return self._thumbnail_url_src

    @property
    def thumbnail_url_small(self):
        return self._thumbnail_url_small

    @property
    def thumbnail_url_medium(self):
        return self._thumbnail_url_medium

    @property
    def thumbnail_url_large(self):
        return self._thumbnail_url_large

    @property
    def subscribed(self):
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
