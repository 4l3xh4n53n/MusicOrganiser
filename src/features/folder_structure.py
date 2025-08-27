"""
This file allows folder structure to be made for different artists and albums
"""
import os.path
import subprocess

from src.config import MUSIC_FOLDER
from src.data.artist import Artist


def generate_folder_structure(artist:Artist):
    # First we must ensure that the Artist folder exists

    artist_folder = f"{MUSIC_FOLDER}/{artist.name}"

    if not os.path.isdir(artist_folder):
        command = ["mkdir", artist_folder]
        subprocess.run(command)

    # Then we can make a folder for each album

    for album in artist.albums:
        # todo If an albums date is changed a second folder will appear

        album_folder = f"{artist_folder}/{album.date} - {album.title}"

        if not os.path.isdir(album_folder):
            command = ["mkdir", album_folder]
            subprocess.run(command)
