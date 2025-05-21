import tkinter as tk

from src.data.album import Album
from src.data.artist_storage import get_artist


class AlbumFrame: # todo, add functions so values can actually be changed.
    def __init__(self, parent_frame, album:Album):
        frame = tk.Frame(parent_frame)
        frame.pack()

        # String values

        album_title = tk.Text(frame, height=1, width=30)
        album_year = tk.Text(frame, height=1, width=6)
        album_type = tk.Text(frame, height=1, width=15)

        # Boolean values

        album_downloading = tk.Checkbutton(frame, text="Downloading", height=1, width=10)
        album_downloaded = tk.Checkbutton(frame, text="Downloaded", height=1, width=10)
        album_tags = tk.Checkbutton(frame, text="Tags", height=1, width=4)
        album_cover = tk.Checkbutton(frame, text="Cover", height=1, width=5)
        album_replay_gain = tk.Checkbutton(frame, text="Replay Gain", height=1, width=9)
        album_server_upload = tk.Checkbutton(frame, text="Server Upload", height=1, width=12)

        # String values

        album_format = tk.Text(frame, height=1, width=8)
        album_markers = tk.Text(frame, height=1, width=6)
        album_notes = tk.Text(frame, height=1, width=40)

        for element in [album_title, album_year, album_type, album_downloading, album_downloaded, album_tags,
                        album_cover, album_replay_gain, album_server_upload, album_format, album_markers, album_notes]:
            element.pack(side="left")

        # Set checkbox states

        checkboxes = [
            (album_downloading, album.downloading),
            (album_downloaded, album.downloaded),
            (album_tags, album.tags),
            (album_cover, album.cover),
            (album_replay_gain, album.replay_gain),
            (album_server_upload, album.server_upload),
        ]

        for box, value in checkboxes:
            box.select() if value else box.deselect()

        album_title.insert(tk.END, album.title)
        album_type.insert(tk.END, album.type)
        album_year.insert(tk.END, str(album.date))
        album_format.insert(tk.END, album.format)
        if album.markers is not None:
            album_markers.insert(tk.END, str(album.markers))
        if album.markers is not None:
            album_notes.insert(tk.END, str(album.notes))


class DataEditingPanel:


    def __init__(self, window:tk.Tk):
        self.selected_artist = None
        data_editor = tk.Frame(window)
        data_editor.pack(side="right", expand=True, padx=10, pady=(10, 10))

        # Artist Editor

        artist_information = tk.Frame(data_editor)
        artist_information.pack(side="top", expand=True, padx=10, pady=(10, 10))

        self.artist_name = tk.Text(artist_information, height=1, width=30)
        self.artist_name.pack(side="left")

        self.artist_markers = tk.Text(artist_information, height=1, width=4)
        self.artist_markers.pack(side="left")

        self.artist_notes = tk.Text(artist_information, height=1, width=50)
        self.artist_notes.pack(side="right")

        # Album Editor

        self.album_editor = tk.Frame(data_editor)
        self.album_editor.pack(side="bottom", expand=True, padx=10, pady=(10,10))


    def set_selected_artist(self, selected_artist_name:str):
        # Set everything to be empty

        for widget in [self.artist_name, self.artist_markers, self.artist_notes]:
            widget.delete("1.0", tk.END)

        # Get the artist
        self.selected_artist = get_artist(selected_artist_name)

        self.artist_name.insert(tk.END, self.selected_artist.name)
        if self.selected_artist.markers is not None:
            self.artist_markers.insert(tk.END, self.selected_artist.markers)
        if self.selected_artist.notes is not None:
            self.artist_notes.insert(tk.END, self.selected_artist.notes)

        for album in self.selected_artist.albums:
            AlbumFrame(self.album_editor, album)
