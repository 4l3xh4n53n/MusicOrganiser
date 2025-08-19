from src.data.artist import Artist
from tests.conftest import make_test_album, make_test_artist, setup_mock_db


patch_target = "src.data.artist.connect_to_database"


class TestArtist:


    def test_from_database(self, mocker):
        """
        Artist.from_database() is supposed to take an artists name and get the corresponding artist
        data from the database and build an Artist object using that data.
        """
        setup_mock_db(mocker, patch_target,
                      {"name": "test_name", "cover": False, "albums": [],"notes": "Test notes", "markers": "G,E"})

        result = Artist.from_database("test_name")

        assert result is not None
        assert result._id is not None
        assert result.name == "test_name"
        assert result.notes == "Test notes"
        assert result.markers == "G,E"


    def test_add_albums(self):
        """
        Artist.add_albums() is supposed to take a list of Albums and add them to the artists list
        of Albums. The function itself uses the Artist.add_album() function, so this test also tests
        that indirectly.
        """
        artist = make_test_artist(albums=[])
        album = make_test_album(title="test_title_1")
        album2 = make_test_album(title="test_title_2")

        artist.add_albums([album, album2])

        assert artist.get_album("test_title_1") is album
        assert artist.get_album("test_title_2") is album2


    def test_get_albums_json(self):
        """
        Artist.get_albums_json() is supposed to return the list of Albums but in JSON/dict format.
        """
        artist = make_test_artist(albums=[])
        album = make_test_album(title="test_title_1")
        album2 = make_test_album(title="test_title_2")
        artist.add_albums([album, album2])

        json = [album.to_dict(), album2.to_dict()]

        assert artist.get_albums_json() == json


    def test_get_album(self):
        """
        Artist.get_album() is supposed to take an album name and get that album from the artists
        list of Albums.
        """
        artist = make_test_artist(albums=[])
        album = make_test_album(title="test_title")

        artist.add_album(album)

        assert artist.get_album("test_title") is album


    def test_to_dict(self, test_artist_data):
        """
        This function turns the Artist object (and Albums) into a JSON/dict object.
        """
        artist = make_test_artist()

        assert artist.to_dict() == test_artist_data # make_test_artist() uses test_artist_data to construct the Artist


    def test_remove_album(self, test_album_data):
        """
        This function is supposed to remove an Album from an Artists Album list
        """
        artist = make_test_artist()
        album = make_test_album()
        artist.add_album(album)

        assert len(artist.albums) == 1 # make sure add albums works

        artist.delete_album(album.title)

        assert len(artist.albums) == 0 # Ensure albums have been removed


    def test_delete(self, mocker):
        """
        This function is supposed to delete an artist from the MongoDB database
        """
        collection = setup_mock_db(mocker, patch_target)

        # Create a fresh new Artist object and save it to the database

        artist = make_test_artist(name="test_name")
        artist.save() # Save the artist to the database

        # Delete the artist from the database
        artist.delete()

        database_search_result = collection.find_one({"_id": artist._id})

        assert database_search_result is None


    def test_save(self, mocker):
        """
        Artist.save() is supposed to save the Artist object to the database in a JSON format.
        The function is supposed to figure out whether the artist already exists in the database, to do
        this it uses the _id value, anything not in the database will not have an _id.
        If it is not in the database it will save a new to the database, if it is in the database it will
        update the document in the database.
        """
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

