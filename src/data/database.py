from contextlib import contextmanager
from typing import Collection, Optional

import pymongo.errors
from pymongo import MongoClient

artist_list: list[str] = None
"""
The purpose of the artist_list is to have a list of artists that can be selected 
from a menu that can then be used for manipulating the artist and associated albums
"""
# todo apparently having all this in not a class is an anti-pattern

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

