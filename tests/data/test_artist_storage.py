from src.data import artist_storage, database
from tests.conftest import setup_mock_db, make_test_artist

patch_target = "src.data.artist.connect_to_database"

class TestArtistStorage:


    def test_get_artist(self, mocker):
        """
        ArtistStorage.get_artist() is supposed to get an artist by their name, it should first
        check the local cache, if it's in the local cache an Artist object will be returned
        immediately, if not, the artist data will be taken from the database and built into
        an Artist object, this should then be stored in the local cache.
        The function is not supposed to be passed invalid artist names (these should be checked before)
        """
        setup_mock_db(mocker, patch_target,
                      {"name": "test_name", "albums": [], "notes": "Test notes", "markers": "G,E"})

        # Get an artist from the database
        artist1 = artist_storage.get_artist("test_name")

        # Get the artist again, this time from the local cache
        artist2 = artist_storage.get_artist("test_name")

        # If the artist was taken from the cache the second time then artist 2 and artist 1 should be the same object
        assert artist2 is artist1


    def test_add_artist(self):
        """
        ArtistStorage.add_artist() is supposed to add an Artist object to the local cache
        of artists.
        """
        test_artist = make_test_artist()
        artist_storage.cache_artist(test_artist)

        assert test_artist in artist_storage.artists
