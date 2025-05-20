from src.data.artist import Artist

artists = []


def get_artist(artist_name:str):
    """
    This function takes the name of an artist and returns an Artist object
    Artist name is case-sensitive, artists should be selected from a list to ensure name is correct
    This function will not handle artist names that aren't in the database
    :param artist_name: The name of the artist to get
    """
    # First, we search for the artist in the artists list
    for artist in artists:
        if artist.name == artist_name:
            return artist

    # If it cannot be found we get the artist from the database

    artist = Artist.from_database(artist_name)
    artists.append(artist)
    return artist

"""
This function adds an artist object to the local list of artists
"""
def add_artist(artist:Artist):
    artists.append(artist)