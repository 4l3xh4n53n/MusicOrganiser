from src.data import database
from tests.conftest import setup_mock_db

patch_target = "src.data.database.connect_to_database"

class TestDatabase:


    def test_get_artist_list(self, mocker):
        """
        Database.get_artist_list() is supposed to get a list names for each artist in the database.
        """
        database.artist_list = None
        setup_mock_db(mocker, patch_target,
                      [{"name": "artist1", "albums": [], "notes": "", "markers": ""},
                            {"name": "artist2", "albums": [], "notes": "", "markers": ""},
                            {"name": "artist3", "albums": [], "notes": "", "markers": ""}])

        artist_list = database.get_artist_list()
        assert set(artist_list) == {"artist1", "artist2", "artist3"}


    def test_filter_artist_list(self):
        """
        Database.filter_artist_list() is supposed to filter the artist_list whilst being
        case-insensitive
        """
        database.artist_list = ["band1", "artist1", "Band2", "Artist2"]
        assert database.filter_artist_list("ban") == ["band1", "Band2"]
        assert database.filter_artist_list("AR") == ["artist1", "Artist2"]

