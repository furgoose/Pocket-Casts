# Pocket-Casts

Unofficial Pocket Casts API writter in Python 3.

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
- pocket. **get_episode_info(uuid, episode_uuid)**
- pocket. **get_podcast_info(uuid, page, sort)**
- pocket. **get_episode_notes(episode_uuid)**
- pocket. **get_subscribed_podcasts()**
- pocket. **get_new_releases()**
- pocket. **get_in_progress()**