import mongomock

from src.data import artist_storage, database
from src.data.artist import Artist


class TestArtistStorage:

    def test_get_artist(self, mocker):
        collection = mongomock.MongoClient().music.music
        collection.insert_one({"name": "test_name", "albums": [], "notes": "Test notes", "markers": "G,E"})
        context_manager = mocker.MagicMock()
        context_manager.__enter__.return_value = collection
        context_manager.__exit__.return_value = None
        mocker.patch("src.data.artist.connect_to_database", return_value=context_manager)

        # Get an artist from the database
        artist1 = artist_storage.get_artist("test_name")

        # Get the artist again, this time from the local cache
        artist2 = artist_storage.get_artist("test_name")

        # If the artist was taken from the cache the second time then artist 2 and artist 1 should be the same object
        assert artist2 is artist1

    def test_add_artist(self):
        test_artist = Artist("test_name", [], "test_notes")
        artist_storage.add_artist(test_artist)

        assert test_artist in artist_storage.artists
