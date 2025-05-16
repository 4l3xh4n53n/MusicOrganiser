import mongomock

from src.data import database


class TestDatabase:
    def test_get_artist_list(self, mocker):
        database.artist_list = None
        collection = mongomock.MongoClient().music.music
        collection.insert_many([{"name": "artist1", "albums": [], "notes": "", "markers": ""},
                                {"name": "artist2", "albums": [], "notes": "", "markers": ""},
                                {"name": "artist3", "albums": [], "notes": "", "markers": ""}])
        context_manager = mocker.MagicMock()
        context_manager.__enter__.return_value = collection
        context_manager.__exit__.return_value = None
        mocker.patch("src.data.database.connect_to_database", return_value=context_manager)

        artist_list = database.get_artist_list()
        assert set(artist_list) == {"artist1", "artist2", "artist3"}

    def test_filter_artist_list(self):
        database.artist_list = ["band1", "artist1", "Band2", "Artist2"]
        assert database.filter_artist_list("ban") == ["band1", "Band2"]
        assert database.filter_artist_list("AR") == ["artist1", "Artist2"]
