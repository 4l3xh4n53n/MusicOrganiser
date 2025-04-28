from pymongo import MongoClient

from constants import ALBUM_LOCATIONS


def connect_to_database():
    client = MongoClient("mongodb://test:test@localhost:27017/")
    return client.music.music

def get_artist(artist:str):
    db = connect_to_database()
    result = db.find_one({"name": artist})
    result.pop("_id") # Remove the _id item as we don't need itd
    return result

"""
This function takes the name of an artist and an album and returns the album information
The reason the artist needs to be passed to the function is because it makes the search
more specific, meaning we do not need to handle any similar album names belonging to 
multiple artists, and don't need to make overly complicated queries to the database.
"""
def get_album(artist_query:str, album_query:str):
    artist_data = get_artist(artist_query)
    album_list = artist_data.get("albums")

    for album_type in ALBUM_LOCATIONS:
        album_type_list = album_list.get(album_type)
        for album in album_type_list:
            if album.get("title").lower() == album_query.lower():
                return album

    return None

def add_artist(artist:str):
    pass

"""
This function adds an album to an artist
This function has the option to add the album and set the downloading status to true
"""
def add_album(artist:str, album:str, year:str, downloading:bool):
    pass

def change_status(album:str, status:str, value:bool):
    pass


# TODO, we need some functions to find albums or artists that are missing stuff or have certain markers

def get_artists_matching_criteria():
    pass

def get_albums_matching_criteria():
    pass
