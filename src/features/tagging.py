"""
This file handles tagging of all music files
"""
import os
import re
import subprocess
from os import path

from src.config import MUSIC_FOLDER

"""
Notes for later:

first change directory (CD)
then select file with "select" command
then "get" to get tags (also works with names)
or "set tagname:value" to set values 
will need to incorporate the search of covers website
"""

def get_sub_directories(active_folder):
    disc_number = 1
    sub_folders = []

    while True:
        if path.isdir(f"{active_folder}/CD{disc_number}"):
            sub_folders.append(f"CD{disc_number}")
        elif path.isdir(f"{active_folder}/CD {disc_number}"):
            sub_folders.append(f"CD {disc_number}")
        else:
            break

        disc_number += 1

    if len(sub_folders) == 0:
        return ["."] # Current directory
    else:
        return sub_folders


def run_command(directory, command, file):
    process = subprocess.run(["kid3-cli", "-c", command, file],
                          capture_output=True,
                          text=True,
                          check=True,
                          cwd=directory)
    return process.stdout


def get_files(directory):
    # todo, put this into config
    audio_file_extensions_higher = (".FLAC", ".MP3", ".OGG", ".M4A", ".AAC", ".ALAC", ".WAV")
    audio_file_extensions_lower = tuple([x.lower() for x in audio_file_extensions_higher])
    audio_file_extensions = audio_file_extensions_lower + audio_file_extensions_higher

    # Sort files
    files = os.listdir(directory)
    files.sort()

    # Remove files that are not audio files
    for file in files:
        if not file.endswith(audio_file_extensions):
            files.remove(file)

    return files


def number_tracks(tracks):
    # This checks the first available track to figure out the numbering format
    # I have never seen one with mixed formats

    first_track_number = tracks[0]["number"]

    if re.fullmatch(r'\d{2}', first_track_number) or re.fullmatch(r'\d', first_track_number):
        # Tracks should be in the correct format
        tracks.sort(key=lambda x: int(x["number"]))


    elif re.fullmatch(r'[A-Z]\d', first_track_number):
        # Format A1, A2, B1, B2, convert to 01, 02, 03

        # Make sure all tracks are in order
        tracks.sort(key=lambda x: (x["number"][0], int(x["number"][1:])))

        # Loop through all tracks setting the track number

        track_number = 1
        for track in tracks:
            track["number"] = str(track_number)
            track_number += 1

    elif not first_track_number or first_track_number.strip() == "":
        # Track number probably doesn't exist, check file names
        # Alternatively we could have hit a misnumbered track, unfortunate but an edge case
        # This program was written to speed up the process, not fully automate it

        first_track_title = tracks[0]["file"]

        dash_split = r'^(?:[A-Za-z]\d{1,2}|\d{1,2})\s*-\s*.+$'
        dot_split = r'^(?:[A-Za-z]\d{1,2}|\d{1,2})\s*\.\s*.+$'

        # Check the first track to find what splits the track number and title

        if re.match(dash_split, first_track_title):
            separator = "-"

        elif re.match(dot_split, first_track_title):
            separator = "."

        else:
            return None # Filename is in an unknown format

        # Apply all track numbers

        for track in tracks:
            filename = track["file"]
            number = filename.split(separator, 1)[0].strip()
            track["number"] = number

        number_tracks(tracks)

    else:
        return None # Number is in an unknown format

    return tracks


def title_tracks(tracks):
    # ensures titles and all exist

    # This might be helpful: title = first_track_title[1].rsplit(".", 1)[0].strip()
    return True


def tag_tracks(artist, album):
    # First check the folder exists

    # todo, make this read a folder format from config.py
    active_folder = f"{MUSIC_FOLDER}/{artist.name}/{album.title} ({album.date})" # todo, change this to new format!

    if not path.isdir(active_folder):
        return "Album folder not found"

    sub_directories = get_sub_directories(active_folder)

    for directory in sub_directories:
        active_directory = f"{active_folder}/{directory}"
        files = get_files(active_directory)

        tracks = []

        # Fetch all necessary metadata first

        for file in files:

            title = run_command(active_directory, "get title", file).replace("\n", "")
            number = run_command(active_directory, "get track", file).replace("\n", "")


            tracks.append({
                "file": file,
                "title": title,
                "number": number,
                "new_file_name": ""
            })

        tracks = number_tracks(tracks)

        # make new file names
        # display those and wait for confirmation

        # set artist
        # set album
        # set date
        # set disc number
        # remove all tags which are not [artist, album, date, genre, track number

    return None
