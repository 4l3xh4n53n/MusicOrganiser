import mongomock

from src.data.album import Album
from src.data.artist import Artist
from tests.test_album import test_album


def create_test_album():
    return Album(
        "test_title",
        1984,
        False,
        True,
        True,
        False,
        True,
        False,
        "FLAC",
        "G,E",
        "Test notes"
    )

def create_test_artist():
    return Artist("test_name", notes="Test notes")

class TestArtist:

    def test_from_database(self, mocker):
        collection = mongomock.MongoClient().music.music
        collection.insert_one({"name": "test_name", "albums": [test_album],"notes": "Test notes", "markers": "G,E"})
        context_manager = mocker.MagicMock()
        context_manager.__enter__.return_value = collection
        context_manager.__exit__.return_value = None
        mocker.patch("src.data.artist.connect_to_database", return_value = context_manager)

        result = Artist.from_database("test_name")

        assert result is not None
        assert result.name == "test_name"
        assert result.notes == "Test notes"
        assert result.markers == "G,E"


    def test_add_albums(self):
        artist = create_test_artist()
        album = create_test_album()
        album2 = create_test_album()
        album2.title = "test_title_2"

        artist.add_albums([album, album2])

        assert artist.get_album("test_title") is album
        assert artist.get_album("test_title_2") is album2


    def test_get_album(self):
        artist = create_test_artist()
        album = create_test_album()
        artist.add_album(album)
        assert artist.get_album("test_title") is album

    def test_to_dict(self):
        artist = create_test_artist()
        assert artist.to_dict() == {"name": "test_name", "albums":[], "notes": "Test notes", "markers": None}

    def test_save(self, mocker):
        collection = mongomock.MongoClient().music.music
        context_manager = mocker.MagicMock()
        context_manager.__enter__.return_value = collection
        context_manager.__exit__.return_value = None
        mocker.patch("src.data.artist.connect_to_database", return_value=context_manager)

        artist = create_test_artist()
        artist.save()

        data = collection.find_one({"name" : "new_artist"})
        assert data == artist.to_dict()