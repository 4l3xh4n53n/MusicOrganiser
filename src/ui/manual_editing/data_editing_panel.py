import tkinter as tk
from copy import deepcopy

from src.data.album import Album
from src.data.artist import Artist
from src.data.artist_storage import get_artist, add_artist
from src.data.database import get_artist_list


# todo, make it so artists can be created
# todo, make it so albums can be added
# todo, all the opposite, delete artists and albums (with "Are you sure" box innit)

class AlbumDataFrame:
    """
    This class has a reproducible frame that displays each piece of album information and allows users to
    edit it. This class should only be created from the DataEditingPanel, as that is where it belongs.
    """


    def __init__(self, parent_frame, album:Album):
        """
        One of these can be made for an Album object, it displays the Albums information and allows it to be
        edited by the user. These will usually be in a list with multiple other Album Frames to make an
        artists discography.
        :param parent_frame: The root object that the list of Albums will be displayed in
        :param album: The Album object which data is going to be displayed and modified
        """
        self.original_title = album.title # This is used to identify the album later in-case the title changes

        # Make variables

        self.title = tk.StringVar(value=album.title)
        self.type = tk.StringVar(value=album.type)
        self.year = tk.StringVar(value=str(album.date))

        self.downloading = tk.BooleanVar(value=album.downloading)
        self.downloaded = tk.BooleanVar(value=album.downloaded)
        self.tags = tk.BooleanVar(value=album.tags)
        self.cover = tk.BooleanVar(value=album.cover)
        self.replay_gain = tk.BooleanVar(value=album.replay_gain)
        self.server_upload = tk.BooleanVar(value=album.server_upload)

        self.format = tk.StringVar(value=album.format)
        self.markers = tk.StringVar(value=album.markers if album.markers is not None else "")
        self.notes = tk.StringVar(value=album.notes if album.notes is not None else "")

        # Make a frame for the album

        self.frame = tk.Frame(parent_frame)
        self.frame.pack()

        # String values

        album_title = tk.Entry(self.frame, width=30, textvariable=self.title)
        album_type = tk.OptionMenu(self.frame, self.type, *["studio_album", "ep", "compilations", "covers", "singles"])
        album_year = tk.Entry(self.frame, width=6, textvariable=self.year)
        album_format = tk.Entry(self.frame, width=8, textvariable=self.format)
        album_markers = tk.Entry(self.frame, width=6, textvariable=self.markers)
        album_notes = tk.Entry(self.frame, width=40, textvariable=self.notes)

        # Boolean values

        album_downloading = tk.Checkbutton(self.frame, text="Downloading", height=1, width=10, variable=self.downloading)
        album_downloaded = tk.Checkbutton(self.frame, text="Downloaded", height=1, width=10, variable=self.downloaded)
        album_tags = tk.Checkbutton(self.frame, text="Tags", height=1, width=4, variable=self.tags)
        album_cover = tk.Checkbutton(self.frame, text="Cover", height=1, width=5, variable=self.cover)
        album_replay_gain = tk.Checkbutton(self.frame, text="Replay Gain", height=1, width=9, variable=self.replay_gain)
        album_server_upload = tk.Checkbutton(self.frame, text="Server Upload", height=1, width=12, variable=self.server_upload)

        # Pack all elements

        for element in [album_title, album_type, album_year, album_downloading,
                        album_downloaded, album_tags, album_cover, album_replay_gain,
                        album_server_upload, album_format, album_markers, album_notes]:
            element.pack(side="left")

        # Make delete button

        delete_button = tk.Button(self.frame, text="Delete")
        delete_button.pack(side="left")

        # todo, Bind the delete button to Artist.albums.remove()


class NewAlbumFrame: # todo, I don't think this needs to be it's own class

    def __init__(self, parent_frame):
        """
        A NewAlbumFrame is an empty frame that allows new Album objects to be added to an Artist and to
        the list of Albums in the DataEditingPanel. It allows the Title, Type, Year, Downloading Status, Markers,
        and Notes to be prefilled.
        :param parent_frame: The root object that the list of Albums will be displayed in
        """

        self.frame = tk.Frame(parent_frame)
        self.frame.pack(side="bottom")
        tk.Label(self.frame, text="Add New Album:").pack(side="left")

        # Make variables

        self.title = tk.StringVar()
        self.type = tk.StringVar()
        self.year = tk.StringVar()
        self.downloading = tk.BooleanVar()
        self.markers = tk.StringVar()
        self.notes = tk.StringVar()

        # Album variable boxes

        album_title = tk.Entry(self.frame, width=30, textvariable=self.title)
        album_type = tk.OptionMenu(self.frame, self.type, *["studio_album", "ep", "compilations", "covers", "singles"])
        album_year = tk.Entry(self.frame, width=10, textvariable=self.year)
        album_downloading = tk.Checkbutton(self.frame, text="Downloading", height=1, width=10, variable=self.downloading)
        album_markers = tk.Entry(self.frame, width=10, textvariable=self.markers)
        album_notes = tk.Entry(self.frame, width=40, textvariable=self.notes)

        # Save new album box

        save_button = tk.Button(self.frame, text="Save", command=self.add_new_album)

        for element in [album_title, album_type, album_year, album_downloading, album_markers, album_notes, save_button]:
            element.pack(side="left")


    def add_new_album(self):
        #todo
        # get the data from the UI
        # put data into album object
        # put album object into artist
        # put new album into album frame
        pass


class DataEditingPanel:
    """
    This class is the right side of the editing screen. Along the top it has the Artist information that
    can be edited. Below the Artist information is the list of Albums belonging to that Artist. These can
    also be modified.
    """


    def __init__(self, window:tk.Tk):
        """
        This function creates the DataEditingPanel, that is displayed on the right-hand side of the manual
        editing screen. This does not take an Artist value as the Artist is updated later.
        :param window: The editing screen
        """
        self.selected_artist = None
        self.album_frames = []
        data_editor = tk.Frame(window)
        data_editor.pack(side="right", expand=True, padx=10, pady=(10, 10))

        # Add new artist

        frame0 = tk.Frame(data_editor)
        frame0.pack(side="top")


        self.new_artist_name = tk.StringVar(value="")
        tk.Entry(frame0, textvariable=self.new_artist_name).pack(side="left")
        tk.Button(frame0, text="Add Artist", command=self.add_new_artist).pack(side="left")


        # Save button and response box

        frame1 = tk.Frame(data_editor)
        frame1.pack(side="top")

        save_button = tk.Button(frame1, text="Write to Database", command=self.update_artist_data)
        save_button.pack(side="left")

        self.response_box = tk.Text(frame1, state="disabled", height=1, width=100)
        self.response_box.pack(side="right", expand=True)

        # Artist Variables

        self.name = tk.StringVar(value="")
        self.markers = tk.StringVar(value="")
        self.notes = tk.StringVar(value="")

        # Artist Editor

        artist_information = tk.Frame(data_editor, background="#2ae85d", padx=10, pady=10)
        artist_information.pack(side="top", fill="both", expand=True)

        tk.Label(artist_information, text="Artist Data: ").pack(side="left")

        tk.Entry(artist_information, width=30, textvariable=self.name).pack(side="left")
        tk.Entry(artist_information, width=4, textvariable=self.markers).pack(side="left")
        tk.Entry(artist_information, width=50, textvariable=self.notes).pack(side="left")

        # Album Editor

        self.album_editor = tk.Frame(data_editor, background="#e8cc2a", padx=10, pady=10)
        self.album_editor.pack(side="top", fill="both", expand=True)

        tk.Label(self.album_editor, text="Albums: ").pack(side="top", anchor="nw")

        self.new_album_creator = NewAlbumFrame(data_editor)


    def send_response_message(self, message:str):
        """
        This function puts a message in the response box that is found in the editing panel
        :param message: The message to be displayed
        """
        self.response_box.config(state="normal")
        self.response_box.delete("1.0", tk.END)
        self.response_box.insert(tk.END, message)
        self.response_box.config(state="disabled")


    def update_artist_data(self):
        """
        This function is called from the "save" button. It will take all Artist and Album data
        from the editing window and save it to the database.
        """
        if self.selected_artist is None:
            self.send_response_message("No artist selected")
            return

        # Set the Artist Data

        self.selected_artist.name = self.name.get()
        self.selected_artist.markers = self.markers.get()
        self.selected_artist.notes = self.notes.get()

        # Set the Data for all albums

        for album_frame in self.album_frames: # Get each album displayed in the editing panel
            album = self.selected_artist.get_album(album_frame.original_title)

            album.title = album_frame.title.get().strip()
            album.type = album_frame.type.get().strip()
            if album_frame.year.get().isdigit():
                album.date = int(album_frame.year.get())
            else:
                self.send_response_message("Date format is not valid")
                return

            album.downloading = album_frame.downloading.get()
            album.downloaded = album_frame.downloaded.get()
            album.tags = album_frame.tags.get()
            album.cover = album_frame.cover.get()
            album.replay_gain = album_frame.replay_gain.get()
            album.server_upload = album_frame.server_upload.get()

            album.format = album_frame.format.get()
            album.markers = album_frame.markers.get().strip()
            album.notes = album_frame.notes.get().strip()

            new_artist = deepcopy(self.selected_artist)
            new_artist._id = None

            self.selected_artist.save()
            self.send_response_message("Saved changes.")

            # todo possible ERROR we need to change the "original title" for each AlbumDataFrame


    def add_new_artist(self):
        # Make sure an Artist with the same name does not already exist

        existing_artists = map(str.lower, get_artist_list())
        new_artist_name = self.new_artist_name.get()

        if new_artist_name.lower() in existing_artists:
            self.send_response_message("Artist already exists")
            return

        # Make the Artist object and add them to the local cache
        new_artist = Artist(self.new_artist_name.get())
        add_artist(new_artist)

        self.set_selected_artist(self.new_artist_name.get())


    def set_selected_artist(self, selected_artist_name:str):
        """
        This function sets the selected artists, this populates all editor boxes with the Artist
        data and corresponding Album data and allows them to be edited.
        :param selected_artist_name: The Artists that is to be edited
        """

        # Set artist data to be empty

        for variable in [self.name, self.markers, self.notes]:
            variable.set("")

        # Remove albums

        for frame in self.album_frames:
            frame.frame.destroy()
            del frame

        self.album_frames.clear()

        # Get the artist
        self.selected_artist = get_artist(selected_artist_name)

        # Set the Entry box variables to artist data

        self.name.set(self.selected_artist.name)
        if self.selected_artist.markers is not None:
            self.markers.set(self.selected_artist.markers)
        if self.selected_artist.notes is not None:
            self.notes.set(self.selected_artist.notes)

        # Create an AlbumFrame for each Album and put it in the editor

        for album in self.selected_artist.albums:
            frame = AlbumDataFrame(self.album_editor, album)
            self.album_frames.append(frame)

        self.send_response_message(f"Selected artist: {self.selected_artist.name}")

