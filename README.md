# Pocket-Casts
---
[![Build Status](https://travis-ci.org/exofudge/Pocket-Casts.svg?branch=master)](https://travis-ci.org/exofudge/Pocket-Casts)
[![Coverage Status](https://coveralls.io/repos/github/exofudge/Pocket-Casts/badge.svg?branch=master)](https://coveralls.io/github/exofudge/Pocket-Casts?branch=master)

Unofficial Pocket Casts API writter in Python 3.
## Installation
```sh
$ pip install pocketcasts-api
```
or clone repo and install from source
```sh
$ python setup.py install
```

## Usage
```python
>>> import pocketcasts
>>> pocket = pocketcasts.Pocketcasts('user@email.com')
# alternatively
>>> pocket = pocketcasts.Pocketcasts('user@email.com', password='optional')
```
### Methods
#### Summary
- pocket. **get_top_charts()**
- pocket. **get_featured()**
- pocket. **get_trending()**
- pocket. **get_episode(podcast, episode_uuid)**
- pocket. **get_podcast(uuid)**
- pocket. **get_podcast_episodes(podcast, sort)**
- pocket. **get_episode_notes(episode_uuid)**
- pocket. **get_subscribed_podcasts()**
- pocket. **get_new_releases()**
- pocket. **get_in_progress()**
- pocket. **get_starred()**
- pocket. **update_starred(podcast, episode, starred)**
- pocket. **update_playing_status(podcast, episode, status)**
- pocket. **update_played_position(podcast, episode, position)**
- pocket. **subscribe_podcast(podcast)**
- pocket. **unsubscribe_podcast(podcast)**
- pocket. **search_podcasts(search_str)**
#### get_top_charts()
Returns the top charts currently on the pocketcasts website, as a list of Podcast classes
```python
>>> pocket = pocketcasts.Pocketcasts('user@email.com')
>>> print(pocket.get_top_charts())
[<class 'pocketcasts.podcast.Podcast'> (
    {'_media_type': 'Audio',
     '_uuid': '3782b780-0bc5-012e-fb02-00163e1b201c',
     '_description': '...',
     '_episodes_sort_order': 3,
     '_url': 'https://www.thisamericanlife.org',
     '_thumbnail_small': '',
     '_thumbnail_url': '...',
     '_author': 'This American Life',
     '_id': '',
     '_language': 'en',
     '_api': <pocketcasts.api.Pocketcasts object at 0x0000016F0E6E6390>,
     '_title': 'This American Life',
     '_categories': ['Society & Culture', 'Arts']}
    ), ...
]
```
#### get_featured()
Returns the featured podcasts currently on the pocketcasts website, as a list of Podcast classes
```python
>>> pocket = pocketcasts.Pocketcasts('user@email.com')
>>> print(pocket.get_featured())
[<class 'pocketcasts.podcast.Podcast'>, ...]
```
#### get_trending()
Returns the trending podcasts currently on the pocketcasts website, as a list of Podcast classes
```python
>>> pocket = pocketcasts.Pocketcasts('user@email.com')
>>> print(pocket.get_trending())
[<class 'pocketcasts.podcast.Podcast'>, ...]
```