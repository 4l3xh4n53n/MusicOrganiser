"""
This file handles tagging of all music files
"""
import os
import re
import subprocess
from os import path

from src.config import MUSIC_FOLDER

class Track:

    def __init__(self, file, title, number, container):
        self.file = file
        self.title = title
        self.number = number
        self.container = container
        self.new_filename = f"{number} - {title}.{container}"


class AlbumProcessingResult:

    def __init__(self, album, sub_directory_count):
        self.album = album
        self.discs = [sub_directory_count]
        self.errors = []


    def add_disc(self, disc_number, tracks):
        self.discs[disc_number] = tracks


    def add_error(self, error):
        self.errors.append(error)


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


def get_track_container(filename):
    return filename.rsplit(".", 1)[1].strip()


def split_filename(filename):
    dash_split = r'^(?:[A-Za-z]\d{1,2}|\d{1,2})\s*-\s*.+$'
    dot_split = r'^(?:[A-Za-z]\d{1,2}|\d{1,2})\s*\.\s*.+$'

    # Check the filename to find what splits the track number and title

    if re.match(dash_split, filename):
        separator = "-"

    elif re.match(dot_split, filename):
        separator = "."

    else:
        return None  # Filename is in an unknown format

    return filename.split(separator, 1)


def get_number_from_filename(filename):
    split_result = split_filename(filename.strip())
    if split_result is None:
        return None # Cannot find track number in filename
    number = split_result[0].strip()
    return number


def get_title_from_filename(filename, container):
    split_result = split_filename(filename.strip())
    if split_result is None:
        # There is no track number the filename is [title].[container]
        title = filename.replace(f".{container}", "")

    else:
        # There is a track number, filename is [track] - [title].[container]
        title = split_result[1].replace(f".{container}", "")

    return title.strip()


def number_tracks(tracks):
    # This checks the first available track to figure out the numbering format
    # I have never seen one with mixed formats

    first_track_number = tracks[0].number

    if first_track_number is None:
        return None # No numbers to base off

    digit = r'\d{1,2}'
    letter_digit = r'[A-Z]\d'

    if re.fullmatch(digit, first_track_number) or re.fullmatch(r'\d', first_track_number):
        # Tracks should be in the correct format
        # Ensure all numbers have 2 digits, I.e. 01, 02, 03...
        for number, track in enumerate(sorted(tracks, key=lambda x: int(x.number)), start=1):
            track.number = f"{number:02}"

    elif re.fullmatch(letter_digit, first_track_number):
        # Format A1, A2, B1, B2, convert to 01, 02, 03

        # Make sure all tracks are in order
        tracks.sort(key=lambda x: (x.number[0], int(x.number[1:])))

        # Loop through all tracks setting the track number

        track_number = 1
        for track in tracks:
            track.number = f"{track_number:02}"
            track_number += 1

    else:
        return None # Number is in an unknown format

    return tracks


def get_disc_number(directory_name):
    if directory_name == ".":
        return 0 # No discs

    # Directory is formatted CD 1 or CD1

    return directory_name[-1]


def tag_tracks(artist, album):
    # First check the folder exists

    # todo, make this read a folder format from config.py
    active_folder = f"{MUSIC_FOLDER}/{artist.name}/{album.title} ({album.date})" # todo, change this to new format!

    if not path.isdir(active_folder):
        return "Album folder not found"

    sub_directories = get_sub_directories(active_folder)

    result = AlbumProcessingResult(album, len(sub_directories))

    for directory in sub_directories:
        active_directory = f"{active_folder}/{directory}"
        files = get_files(active_directory)

        tracks = []

        # Fetch all necessary metadata first

        for file in files:

            container = get_track_container(file)
            title = run_command(active_directory, "get title", file).replace("\n", "")
            number = run_command(active_directory, "get track", file).replace("\n", "")

            if title == "":
                title = get_title_from_filename(file, container)

            if number == "":
                number = get_number_from_filename(file)
                if number is None:
                    result.add_error(f"Cannot find track number for: {file}")

            # todo, if these fail, prompt to add them manually!

            tracks.append(Track(file, title, number, container))

        tracks = number_tracks(tracks)
        disc_number = get_disc_number(directory)

        result.add_disc(disc_number, tracks)

    return result

        # display those and wait for confirmation (showing original)

        # set artist
        # set album
        # set date
        # set disc number
        # remove all tags which are not [artist, album, date, genre, track number


