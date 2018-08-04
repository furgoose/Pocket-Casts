import pytest
import os

USERNAME = os.environ.get('POCKETCAST_USER')
PASSWORD = os.environ.get('POCKETCAST_PASSWORD')

if USERNAME == None or PASSWORD == None:
    pytest.skip('No environment variables', allow_module_level=True)

@pytest.fixture(scope="module")
def client():
    import pocketcasts

    c = pocketcasts.Pocketcasts()
    c.login(USERNAME, PASSWORD)
    return c

def test_get_episode(client):
    episode = client.get_episode("7b28c700-d4f1-0134-ebdd-4114446340cb")
    assert type(episode) == client.Episode

def test_get_podcast(client):
    client.get_podcast('12012c20-0423-012e-f9a0-00163e1b201c')

def test_get_episode_notes(client):
    client.get_episode_notes('a35748e0-bb4d-0134-10a8-25324e2a541d')

def test_get_subscribed_podcasts(client):
    client.get_subscribed_podcasts()

def test_get_new_releases(client):
    client.get_new_releases()

def test_get_in_progress(client):
    client.get_in_progress()

def test_get_starred(client):
    client.get_starred()

def test_update_starred(client):
    client.update_starred('2e0eb560-5950-0136-fa7c-0fe84b59566d', 'e92551b1-8eda-4cb1-9f04-4b3dea78829a', True)
    episode = client.get_episode('e92551b1-8eda-4cb1-9f04-4b3dea78829a')
    assert episode.starred == True
    client.update_starred('2e0eb560-5950-0136-fa7c-0fe84b59566d', 'e92551b1-8eda-4cb1-9f04-4b3dea78829a', False)
    episode.update()
    assert episode.starred == False

def test_queue_play_now(client):
    client.queue_play_now('2e0eb560-5950-0136-fa7c-0fe84b59566d', 'e92551b1-8eda-4cb1-9f04-4b3dea78829a')

def test_queue_play_next(client):
    client.queue_play_next('2e0eb560-5950-0136-fa7c-0fe84b59566d', 'e92551b1-8eda-4cb1-9f04-4b3dea78829a')

def test_get_queue(client):
    queue = client.get_queue()
    assert type(queue) == list

def test_subscribe_unsubscribe_podcast(client):
    client.subscribe_podacast('2e0eb560-5950-0136-fa7c-0fe84b59566d')
    client.unsubscribe_podacast('2e0eb560-5950-0136-fa7c-0fe84b59566d')
