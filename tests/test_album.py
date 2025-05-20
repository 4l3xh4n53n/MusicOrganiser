from src.data.album import Album


class TestAlbum:

    def test_to_dict(self, test_album_data):
        new_album = Album.from_dict(test_album_data)

        assert new_album.to_dict() == test_album_data

