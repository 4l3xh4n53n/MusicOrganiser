from src.data.album import Album


test_album = {
            "title": "test_title",
            "type": "studio_album",
            "date": 1984,
            "downloading": False,
            "downloaded": True,
            "tags": True,
            "cover": False,
            "replay_gain": True,
            "server_upload": False,
            "format": "FLAC",
            "markers": "G,E",
            "notes": "You can write notes here!"
}

class TestAlbum:

    def test_to_dict(self):
        new_album = Album.from_dict(test_album)

        assert new_album.to_dict() == test_album

