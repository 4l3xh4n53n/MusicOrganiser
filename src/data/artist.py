from src.data.album import Album
from src.data.database import connect_to_database


class Artist:
    """
    Represents an artist contains a list of albums and some useful metadata
    """
    albums = []

    def __init__(self, name:str, albums:list[Album] = None, notes:str = None, markers:str = None, _id = None):
        """
        Initialises a new Artist instance
        :param name: The name of the artist
        :param albums: A list of albums
        :param notes: Some useful notes
        :param markers: Contains information to help keep track of Artists
        :param _id: The MongoDB _ID value, should be None when creating a new artist
        """
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
        """
        Gets an artist from the MongoDB database
        :param name: The name of the artist
        :return: An Artist object with the data from the database
        """
        with connect_to_database() as db:
            data = db.find_one({"name": name})
            if data is None:
                return None

        return cls(name, data.get("albums"), data.get("notes"), data.get("markers"), data.get("_id"))


    def get_album(self, name:str):
        """
        Gets an Album object belonging to this artist
        :param name: The albums name
        :return: The Album
        """
        for album in self.albums:
            if album.title.lower() == name.lower():
                return album

        return None


    def get_albums_json(self):
        """
        Gets all albums in JSON format
        Useful for storing an album list in MongoDB
        :return: A list of albums
        """
        json = []
        for album in self.albums:
            json.append(album.to_dict())
        return json


    def add_album(self, album:Album):
        """
        Adds an album
        :param album: The new album
        """
        self.albums.append(album)


    def add_albums(self, albums:list[Album]):
        """
        Adds multiple albums
        :param albums: A list of Albums
        """
        for album in albums:
            self.albums.append(album)


    def to_dict(self):
        """
        Creates a dictionary object of the artist, including albums (also in dictionary form)
        Useful for storing an artist in MongoDB
        :return: Dictionary consisting of Artist data
        """
        return {
            "_id": self._id,
            "name": self.name,
            "albums": self.get_albums_json(),
            "notes": self.notes,
            "markers": self.markers,
        }


    def delete_album(self, name:str):
        """
        Removes an album from the Artists Album list
        :param name: The name of the Album
        """
        for album in self.albums:
            if album.title.lower() == name.lower():
                self.albums.remove(album)


    def delete(self):
        """
        Removes the Artist from the MongoDB database.
        """
        with connect_to_database() as db:
            if self._id is None:
                return # Artist was never in the database

            db.delete_one({
                "_id": self._id
            })


    def save(self):
        """
        Saves the Artist to the MongoDB database.
        This function will figure out whether an artist is new or already exists.
        DO NOT create a new instance of an artist that already exists in the database.
        """
        with connect_to_database() as db:
            if self._id is None: # Artist does not exist in the database. Create a new one
                db.insert_one({
                    "name": self.name,
                    "albums": self.get_albums_json(),
                    "markers": self.markers,
                    "notes": self.notes
                })

                self._id = db.find_one({"name": self.name})["_id"]

            else: # Artist already exists in the database
                db.replace_one({"_id": self._id},{
                    "name": self.name,
                    "albums": self.get_albums_json(),
                    "markers": self.markers,
                    "notes": self.notes
                })





