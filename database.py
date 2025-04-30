from contextlib import contextmanager
from typing import Collection, Optional

import pymongo.errors
from pymongo import MongoClient

from constants import ALBUM_LOCATIONS

"""
This function allows you to connect and query the database
"""
@contextmanager
def connect_to_database() -> Collection:
    client = None
    try:
        client = MongoClient("mongodb://test:test@localhost:27017/")
        collection = client.music.music
        yield collection
    except pymongo.errors.ConnectionFailure as error:
        print(f"Error: {error}")
    finally:
        client.close()


"""
This function takes the name of an artist and returns all information about them,
this information includes: albums, notes and markers
"""
def get_artist(artist:str):
    with connect_to_database() as db:
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

    # Search all subtypes in the albums list until the album with the correct title is found

    for album_type in ALBUM_LOCATIONS:
        album_type_list = album_list.get(album_type)
        for album in album_type_list:
            if album.get("title") == album_query:
                return album

    return None

"""
This function adds an empty artist object to the database
it can also add markers and notes to the artist
for markers and notes, see the documentation in main.py
"""
def add_artist(artist:str, markers:str = None, notes:str = None):
    with connect_to_database() as db:
        db.insert_one({
            "name": artist,
            "albums": {
                "studio_albums": [],
                "eps": [],
                "compilation_albums": [],
                "cover_albums": [],
                "singles": [],
            },
            "markers": markers,
            "notes": notes
        })


"""
This function adds an album to an artist
This function has the option to add the album and set the downloading status to true
it can also add markers and notes to the album
for markers and notes, see the documentation in main.py
"""
def add_album(artist:str, album_type:str , album:str, year:str, downloading:bool, markers:str = None, notes:str = None):
    album_json = {
        "title": album,
        "date": year,
        # The option to set the album to downloading is given to save database calls and make things faster
        "downloading": downloading,
        "downloaded": False,
        "tags": False,
        "cover": False,
        "replay_gain": False,
        "server_upload": False,
        "format": False,
        "markers": markers,
        "notes": notes
    }

    update_json = {
        "$push": {
            f"albums.{album_type}" : album_json
        }
    }

    with connect_to_database() as db:
        db.update_one({"name":artist}, update_json)


"""
This function changes data values
For example, the status of whether or not an album is downloading can be changed to yes or no
it can also change notes and markers
"""
def change_status(artist:str, album_type:str, album:str,
                  downloading:Optional[bool]=None,
                  downloaded:Optional[bool]=None,
                  tags:Optional[bool]=None,
                  cover:Optional[bool]=None,
                  replay_gain:Optional[bool]=None,
                  server_upload:Optional[bool]=None,
                  format:Optional[str]=None,
                  markers:Optional[str]=None,
                  notes:Optional[str]=None):

    # List of values that could potentially be passed to the function
    potential_updates = {
        "downloading": downloading, "downloaded": downloaded, "tags": tags, "cover": cover, "replay_gain": replay_gain,
        "server_upload": server_upload, "format": format, "markers": markers, "notes": notes
    }

    updates = {}

    for field, value in potential_updates.items():
        if value is not None:
            path = f"albums.{album_type}.$[elem].{field}"
            updates[path] = value

    with connect_to_database() as db:
        db.update_one({"name":artist}, {"$set": updates}, array_filters=[{"elem.title": album}])


"""
This function allows the notes and markers associated with an artist to be changed
"""
def change_artist(artist:str,
                  markers:str=None,
                  notes:str=None):

    # List of values that could potentially be passed to the function
    potential_updates = {
        "markers": markers,
        "notes": notes
    }

    updates = {}

    # Check if a value has been passed to this function, if it has store the value to be updated later
    for field, value in potential_updates.items():
        if value is not None:
            path = f"{field}"
            updates[path] = value

    with connect_to_database() as db:
        db.update_one({"name": artist}, {"$set": updates})


# TODO, we need some functions to find albums or artists that are missing stuff or have certain markers

def get_artists_matching_criteria():
    pass

def get_albums_matching_criteria():
    pass
