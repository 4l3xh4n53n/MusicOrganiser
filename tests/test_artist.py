from src.data.artist import Artist
from tests.conftest import make_test_album, make_test_artist, setup_mock_db


patch_target = "src.data.artist.connect_to_database"

class TestArtist:

    def test_from_database(self, mocker):
        setup_mock_db(mocker, patch_target,
                      {"name": "test_name", "albums": [],"notes": "Test notes", "markers": "G,E"})

        result = Artist.from_database("test_name")

        assert result is not None
        assert result._id is not None
        assert result.name == "test_name"
        assert result.notes == "Test notes"
        assert result.markers == "G,E"


    def test_add_albums(self):
        artist = make_test_artist()
        album = make_test_album(title="test_title_1")
        album2 = make_test_album(title="test_title_2")

        artist.add_albums([album, album2])

        assert artist.get_album("test_title_1") is album
        assert artist.get_album("test_title_2") is album2


    def test_get_albums_json(self):
        artist = make_test_artist()
        album = make_test_album(title="test_title_1")
        album2 = make_test_album(title="test_title_2")
        artist.add_albums([album, album2])

        json = [album.to_dict(), album2.to_dict()]

        assert artist.get_albums_json() == json


    def test_get_album(self):
        artist = make_test_artist()
        album = make_test_album(title="test_title")

        artist.add_album(album)

        assert artist.get_album("test_title") is album


    def test_to_dict(self, test_artist_data):
        artist = make_test_artist()

        assert artist.to_dict() == test_artist_data

    def test_save(self, mocker):
        collection = setup_mock_db(mocker, patch_target)

        # Create a fresh new Artist object and save it to the database

        artist = make_test_artist(name="test_name")
        artist.save()

        # After saving the new artist to the database it should have an ID

        original = collection.find_one({"name" : "test_name"})
        database_id = original.get("_id")

        artist._id = database_id # set old artist ID for comparison with new artist ID

        # Make a new artist to ensure the same artist gets saved

        artist2 = Artist.from_database("test_name")
        artist2.name = "different_name"
        artist2.save()

        # grab fresh from the database then ensure it has the same ID

        artist3 = collection.find_one({"name" : artist2.name})

        assert original == artist.to_dict() # Ensure it is saved correctly
        assert artist3.get("_id") == database_id # Ensure its saved consistently
        assert collection.count_documents({}) == 1 # Ensure no duplicates