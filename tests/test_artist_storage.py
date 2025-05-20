from src.data import artist_storage, database
from tests.conftest import setup_mock_db, make_test_artist

patch_target = "src.data.artist.connect_to_database"

class TestArtistStorage:

    def test_get_artist(self, mocker):
        setup_mock_db(mocker, patch_target,
                      {"name": "test_name", "albums": [], "notes": "Test notes", "markers": "G,E"})

        # Get an artist from the database
        artist1 = artist_storage.get_artist("test_name")

        # Get the artist again, this time from the local cache
        artist2 = artist_storage.get_artist("test_name")

        # If the artist was taken from the cache the second time then artist 2 and artist 1 should be the same object
        assert artist2 is artist1

    def test_add_artist(self):
        test_artist = make_test_artist()
        artist_storage.add_artist(test_artist)

        assert test_artist in artist_storage.artists
