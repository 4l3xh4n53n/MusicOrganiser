from src.data.album import Album
from src.data.database import connect_to_database


class Artist:
    albums = []

    def __init__(self, name, albums = None, notes = None, markers = None):
        self.name = name
        self.notes = notes
        self.markers = markers
        if albums is not None:
            for album in albums:
                Album.from_dict(album)


    @classmethod
    def from_database(cls, name):
        with connect_to_database() as db:
            data = db.find_one({"name": name})
            if data is None:
                return None

        return cls(name, data.get("albums"), data.get("notes"), data.get("markers"))


    def get_album(self, name):
        for album in self.albums:
            if album.title.lower() == name.lower():
                return album

        return None


    def add_album(self, album:Album): # todo, should this be changed to add albums? or a separate func be made?
        self.albums.append(album)


    def to_dict(self):

        albums_as_dict = []

        for album in self.albums:
            albums_as_dict.append(album.to_dict())

        return {
            "name": self.name,
            "albums": self.albums,
            "notes": self.notes,
            "markers": self.markers,
        }


    def save(self):
        pass
        # todo, check database for me
        # todo, either update or insert me




