from src.data.artist_storage import ArtistStorage
from tests.conftest import setup_mock_db, sample_artist


class TestArtistStorage:


    def test_get_artist(self, mocker):
        """
        ArtistStorage.get_artist() is supposed to get an artist by their name, it should first
        check the local cache, if it's in the local cache an Artist object will be returned
        immediately, if not, the artist data will be taken from the database and built into
        an Artist object, this should then be stored in the local cache.
        The function is not supposed to be passed invalid artist names (these should be checked before)
        """
        setup_mock_db(mocker, "src.data.artist.connect_to_database",
                      {"name": "test_name", "albums": [], "notes": "Test notes", "markers": "G,E"})

        setup_mock_db(mocker, "src.data.database.connect_to_database",
                      {"name": "test_name", "albums": [], "notes": "Test notes", "markers": "G,E"})

        test_artist_storage = ArtistStorage()

        # Get an artist from the database
        artist1 = test_artist_storage.get_artist("test_name")

        # Get the artist again, this time from the local cache
        artist2 = test_artist_storage.get_artist("test_name")

        # If the artist was taken from the cache the second time then artist 2 and artist 1 should be the same object
        assert artist2 is artist1


    def test_create_artist(self, mocker):
        """
        ArtistStorage.add_artist() is supposed to add an Artist object to the local cache
        of artists.
        """
        # Mocking get_artist_list because mocking the database created a state leak that I could not find
        mocker.patch("src.data.artist_storage.get_artist_list", return_value=[])

        test_artist_storage = ArtistStorage()

        test_artist_storage.create_artist(
            artist_name=sample_artist.get("name"),
            artist_albums=sample_artist.get("albums"),
            artist_markers=sample_artist.get("markers"),
            artist_notes=sample_artist.get("notes")
        )

        assert sample_artist == test_artist_storage.artist_cache[0].to_dict()
        assert sample_artist.get("name") in test_artist_storage.get_selectable_artists()


    def test_remove_artist(self, mocker):
        mocker.patch("src.data.artist_storage.get_artist_list", return_value=[])

        test_artist_storage = ArtistStorage()

        # Create an Artist

        test_artist = test_artist_storage.create_artist(
            artist_name=sample_artist.get("name"),
            artist_albums=sample_artist.get("albums"),
            artist_markers=sample_artist.get("markers"),
            artist_notes=sample_artist.get("notes")
        )

        test_artist_storage.delete_artist(test_artist)

        assert len(test_artist_storage.artist_cache) is 0
        assert len(test_artist_storage.selectable_artists) is 0


    def test_get_selectable_artists(self, mocker):
        test_names = [
            "artist_1",
            "ARTIST_2",
            "band_1",
            "BanD_2"
        ]
        mocker.patch("src.data.artist_storage.get_artist_list", return_value=test_names)

        test_artist_storage  = ArtistStorage()

        assert test_artist_storage.get_selectable_artists() == test_names
        assert test_artist_storage.get_selectable_artists("artist_2") == ["ARTIST_2"]
        assert test_artist_storage.get_selectable_artists("band") == ["band_1", "BanD_2"]


