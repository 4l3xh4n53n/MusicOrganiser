from src.data.album import Album
from src.data.database import connect_to_database


class Artist:
    albums = []

    def __init__(self, name, albums = None, notes = None, markers = None, _id = None):
        self.name = name
        self.notes = notes
        self.markers = markers
        self.albums = []
        self._id = _id
        if albums is not None:
            for album in albums:
                self.albums.append(Album.from_dict(album))


    @classmethod
    def from_database(cls, name):
        with connect_to_database() as db:
            data = db.find_one({"name": name})
            if data is None:
                return None

        return cls(name, data.get("albums"), data.get("notes"), data.get("markers"), data.get("_id"))


    def get_album(self, name:str):
        for album in self.albums:
            if album.title.lower() == name.lower():
                return album

        return None


    def get_albums_json(self):
        json = []
        for album in self.albums:
            json.append(album.to_dict())
        return json


    def add_album(self, album:Album):
        self.albums.append(album)


    def add_albums(self, albums:list[Album]):
        for album in albums:
            self.albums.append(album)


    def to_dict(self):
        return {
            "_id": self._id,
            "name": self.name,
            "albums": self.get_albums_json(),
            "notes": self.notes,
            "markers": self.markers,
        }


    def save(self):
        with connect_to_database() as db:
            if self._id is None: # Artist does not exist in the database. Create a new one
                db.insert_one({
                    "name": self.name,
                    "albums": self.albums,
                    "markers": self.markers,
                    "notes": self.notes
                })
            else: # Artist already exists in the database
                db.replace_one({"_id": self._id},{
                    "name": self.name,
                    "albums": self.albums,
                    "markers": self.markers,
                    "notes": self.notes
                })





