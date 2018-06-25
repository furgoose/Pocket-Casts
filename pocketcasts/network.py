class _Network(object):
    """Class for podcast networks"""

    def __init__(self, id, **kwargs):
        """

        Args:
            **kwargs: Information about the network
        """
        self._id = id

        self.update(**kwargs)
        
    def update(self, **kwargs):
        self._title = kwargs.get('title')
        self._list = kwargs.get('list')
        self._description = kwargs.get('description')
        self._image_url = kwargs.get('image_url')
        self._color = kwargs.get('color')

    def __repr__(self):
        return f"{self.__class__} ({self.title})"

    @property
    def id(self):
        """Get the network ID"""
        return self._id

    @property
    def title(self):
        """Get the network title"""
        return self._title

    @property
    def list(self):
        """Get the network list"""
        return self._list

    @property
    def description(self):
        """Get the network description"""
        return self._description

    @property
    def image_url(self):
        """Get the network image url"""
        return self._image_url

    @property
    def color(self):
        """Get the network color"""
        return self._color
