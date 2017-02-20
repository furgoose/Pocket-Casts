import pocketcasts
from distutils.core import setup

setup(
    name="pocketcasts-api",
    py_modules=['pocketcasts'],
    version=pocketcasts.__version__,
    description=pocketcasts.__doc__,
    author=pocketcasts.__author__,
    author_email='ferguslongley@live.com',
    url=pocketcasts.__url__,
    download_url='',
    keywords=['podcasts', 'pocketcasts'],
    classifiers=[], requires=['requests']
)