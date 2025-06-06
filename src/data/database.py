from contextlib import contextmanager
from typing import Collection, Optional

import pymongo.errors
from pymongo import MongoClient

artist_list: list[str] = None
"""
The purpose of the artist_list is to have a list of artists that can be selected 
from a menu that can then be used for manipulating the artist and associated albums
"""
# todo, we could just load the artist_list from the database at the start of the program, rather than check everytime
# todo, would this be more appropriate to be loaded into artist_storage?


@contextmanager
def connect_to_database() -> Collection:
    """
    This function allows you to connect to and query the database
    """
    client = None
    try:
        client = MongoClient("mongodb://test:test@localhost:27017/")
        collection = client.music.music
        yield collection
    except pymongo.errors.ConnectionFailure as error:
        print(f"Error: {error}")
    finally:
        client.close()


def filter_artist_list(search_term:str):
    """
    This can filter the list of artists gotten from get_artist_list
    :param search_term: filter
    :return: Filtered list of artists
    """
    global artist_list
    return [
        name for name in artist_list if search_term.lower() in name.lower()
    ]
    # todo, could this function be better?
    # todo, change unicodes, remove spaces
    # todo, also consider making it inclusive and exclusive


def get_artist_list():
    """
    Gets the list of all current artists in the database
    This can be useful for selecting artists, or for comparison when making new artists
    :return: List of artists
    """
    global artist_list
    if artist_list is None:
        with connect_to_database() as db:
            artist_list = db.distinct("name")

    return artist_list


def add_to_artist_list(artist_name:str):
    """
    This function adds an artists name to the list of artists which can be used for searching
    and selecting artists for editing.
    This function does not check for duplicates
    :param artist_name: The name of the new artist
    """
    global artist_list
    artist_list.append(artist_name)


def remove_from_artist_list(artist_name:str):
    """
    This function removes an artists name from the list of artists.
    :param artist_name: The name of the artist
    """
    global artist_list
    artist_list.remove(artist_name)


def get_artists_matching_criteria(markers:str):
    """
    Gets a list of artists matching a certain criteria, the only criteria for Artists is markers
    :param markers: Tracking markers
    :return: A list of artists that match the criteria in JSON format
    """
    with connect_to_database() as db:
        result = db.find({"markers" : {"$regex" : markers}})
        result = list(result)
    return result


def get_albums_matching_criteria( # todo find a way to exclude format
        downloading:Optional[bool]=None,
        downloaded:Optional[bool]=None,
        tags:Optional[bool]=None,
        cover:Optional[bool]=None,
        replay_gain:Optional[bool]=None,
        server_upload:Optional[bool]=None,
        format:Optional[str]=None,
        markers:Optional[str]=None,
        notes:Optional[str]=None):
    """
    Gets a list of albums matching a certain criteria
    For parameters, see the documentation in artist.py
    :return: A list of albums that match the criteria in JSON format
    """

    potential_filters = {
        "downloading": downloading, "downloaded": downloaded, "tags": tags, "cover": cover, "replay_gain": replay_gain,
        "server_upload": server_upload, "format": format, "markers": markers,
        "notes": notes
    }

    filters = []
    projection_filters = [] # A second set of filters formatted differently
    # Sorry this code sucks

    for field, value in potential_filters.items():
        if value is not None:
            filters.append({f"albums.{field}": value})
            projection_filters.append({"$eq":[f"$$album.{field}", value]})

    pipeline = [
        # This filters down to only artists with matching albums
        {
            "$match": {
                "$and": filters
            }
        },
        # This filters down the artists and albums to only include matching albums
        {
            "$project": {
                "_id": 0,
                "name": 1,
                "albums": {
                    "$filter": {
                        "input": "$albums",
                        "as": "album",
                        "cond": {
                            "$and": projection_filters
                        }
                    }
                }
            }
        }
    ]

    with connect_to_database() as db:
        results = list(db.aggregate(pipeline))
    return results

