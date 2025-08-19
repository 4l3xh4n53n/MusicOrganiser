import mongomock
import pytest

from src.data.album import Album
from src.data.artist import Artist


def setup_mock_db(mocker, patch_target, data=None):
    collection = mongomock.MongoClient().music.music

    if data is not None:
        if type(data) is list:
            collection.insert_many(data)
        else:
            collection.insert_one(data)

    context_manager = mocker.MagicMock()
    context_manager.__enter__.return_value = collection
    context_manager.__exit__.return_value = None
    mocker.patch(patch_target, return_value=context_manager)

    return collection


sample_album = {
        "title": "test_title",
        "type": "studio_album",
        "date": 1984,
        "downloading": False,
        "downloaded": True,
        "tags": True,
        "cover": False,
        "replay_gain": True,
        "server_upload": False,
        "format": "FLAC",
        "markers": "G,E",
        "notes": "You can write notes here!"
}


@pytest.fixture
def test_album_data():
    return sample_album.copy()


def make_test_album(**overrides):
    album = sample_album.copy()
    album.update(overrides)
    return Album.from_dict(album)


sample_artist = {
    "_id": None,
    "name": "test_name",
    "albums": [],
    "cover": False,
    "markers": "",
    "notes": "Test notes"
}


@pytest.fixture
def test_artist_data():
    return sample_artist.copy()


def make_test_artist(**overrides):
    artist = sample_artist.copy()
    artist.update(overrides)
    return Artist(
        artist.get("name"),
        artist.get("albums"),
        artist.get("cover"),
        artist.get("notes"),
        artist.get("markers")
    )
