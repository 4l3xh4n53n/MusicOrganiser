from src.data.artist import Artist

artists = []

"""
This function takes the name of an artist and returns an Artist object
"""
def get_artist(artist_name:str):
    for artist in artists:
        if artist.name == artist_name:
            return artist

    return None


"""
This function adds an artist object to the local list of artists
"""
def add_artist(artist:Artist):
    artists.append(artist)