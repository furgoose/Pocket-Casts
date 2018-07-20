import pytest

@pytest.fixture(scope="module")
def client():
    import pocketcasts

    return pocketcasts.Pocketcasts()

def test_get_top(client):
    client.get_top()

def test_get_featured(client):
    client.get_featured()

def test_get_trending_podcasts(client):
    client.get_trending_podcasts()

def test_get_trending_episodes(client):
    client.get_trending_episodes()

def test_get_new(client):
    client.get_new()

def test_get_discover(client):
    client.get_discover()

def test_get_networks(client):
    client.get_networks()

@pytest.mark.xfail
def test_get_episode(client):
    episode = client.get_episode("7b28c700-d4f1-0134-ebdd-4114446340cb")
    assert type(episode) == client.Episode

@pytest.mark.xfail
def test_get_podcast(client):
    client.get_podcast('12012c20-0423-012e-f9a0-00163e1b201c')

@pytest.mark.xfail
def test_get_episode_notes(client):
    client.get_episode_notes('a35748e0-bb4d-0134-10a8-25324e2a541d')

@pytest.mark.xfail
def test_get_subscribed_podcasts(client):
    client.get_subscribed_podcasts()

@pytest.mark.xfail
def test_get_new_releases(client):
    client.get_new_releases()

@pytest.mark.xfail
def test_get_in_progress(client):
    client.get_in_progress()

@pytest.mark.xfail
def test_get_starred(client):
    client.get_starred()

@pytest.mark.xfail
def test_update_starred(client):
    client.update_starred('2e0eb560-5950-0136-fa7c-0fe84b59566d', 'e92551b1-8eda-4cb1-9f04-4b3dea78829a', True)
    episode = client.get_episode('e92551b1-8eda-4cb1-9f04-4b3dea78829a')
    assert episode.starred == True
    client.update_starred('2e0eb560-5950-0136-fa7c-0fe84b59566d', 'e92551b1-8eda-4cb1-9f04-4b3dea78829a', False)
    episode.update()
    assert episode.starred == False

@pytest.mark.xfail
def test_queue_play_now(client):
    client.queue_play_now('2e0eb560-5950-0136-fa7c-0fe84b59566d', 'e92551b1-8eda-4cb1-9f04-4b3dea78829a')

@pytest.mark.xfail
def test_queue_play_next(client):
    client.queue_play_next('2e0eb560-5950-0136-fa7c-0fe84b59566d', 'e92551b1-8eda-4cb1-9f04-4b3dea78829a')

@pytest.mark.xfail
def test_get_queue(client):
    queue = client.get_queue()
    assert type(queue) == list