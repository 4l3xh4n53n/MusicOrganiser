from src.data.artist import Artist
from src.data.database import get_artist_list


class ArtistStorage:
    """
    This class is in charge of storing all Artist objects, making them accessible to the rest of the
    program. It also maintains a list of Artists that can be selected from.
    """

    def __init__(self):
        self.artist_cache : list[Artist] = []
        self.selectable_artists : list[str] = get_artist_list()


    def get_artist(self, artist_name:str):
        """
        This function takes the name of an artist and returns an Artist object
        Artist name is case-sensitive, artists should be selected from a list to ensure name is correct
        This function will not handle artist names that aren't in the database
        :param artist_name: The name of the artist to get
        """
        # First, we search for the artist in the artists list
        for artist in self.artist_cache:
            if artist.name == artist_name:
                return artist

        # If it cannot be found we get the artist from the database

        artist = Artist.from_database(artist_name)
        self.artist_cache.append(artist)
        return artist

    def create_artist(self, artist_name = None, artist_albums = None, artist_markers = None, artist_notes = None):
        """
        This function creates a new Artist object and adds them to the cache and list of selectable artists.
        All variables must be error checked and sanitised before being passed to the function
        :param artist_name: The name of the Artist
        :param artist_albums: The Artists albums
        :param artist_markers: The Artists markers
        :param artist_notes: The Artists notes
        :return: Newly created Artist object
        """
        artist = Artist(name=artist_name, albums=artist_albums, markers=artist_markers, notes=artist_notes)
        self.artist_cache.append(artist)
        self.selectable_artists.append(artist_name)
        return artist


    def get_selectable_artists(self, search_term:str = None):
        """
        This function returns a list of names of selectable artists.
        :param search_term: Filters the list of selectable artists
        :return: Filtered list of artists
        """
        if search_term is None:
            return self.selectable_artists

        return [
            name for name in self.selectable_artists if search_term.lower() in name.lower()
        ]
        # todo, could this function be better?
        # todo, change unicodes, remove spaces
        # todo, also consider making it inclusive and exclusive


    def delete_artist(self, artist: Artist):
        """
        This function fully deletes an artist from everywhere in the program.
        This includes the list of artists, the database, and the list of selectable artists
        :param artist: The Artist to be deleted
        """
        self.artist_cache.remove(artist)
        artist.delete()
        self.selectable_artists.remove(artist.name)

