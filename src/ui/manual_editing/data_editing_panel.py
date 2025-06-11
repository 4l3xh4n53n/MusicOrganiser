import tkinter as tk
from copy import deepcopy

from src.data.album import Album
from src.data.artist import Artist
from src.data.artist_storage import ArtistStorage


class AlbumDataFrame:
    """
    This class has a reproducible frame that displays each piece of album information and allows users to
    edit it. This class should only be created from the DataEditingPanel, as that is where it belongs.
    """


    def __init__(self, parent_frame, album:Album, selected_artist:Artist, album_frame_list):
        """
        One of these can be made for an Album object, it displays the Albums information and allows it to be
        edited by the user. These will usually be in a list with multiple other Album Frames to make an
        artists discography.
        :param parent_frame: The root object that the list of Albums will be displayed in
        :param album: The Album object which data is going to be displayed and modified
        """

        # todo, RE_WRITE INNIT

        # Get all variables belonging to an Album object

        vars(album) # todo, I think this needs to be filtered

        self.album_frame_list = album_frame_list
        self.selected_artist = selected_artist
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

        album_downloading = tk.Checkbutton(self.frame, text="Downloading", bg="red", activebackground="green", height=1, width=10, variable=self.downloading)
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

        delete_button = tk.Button(self.frame, text="Delete", command=self.delete_album)
        delete_button.pack(side="left")

        # Set the background of each button to change

        for check_value, check_box in [(self.downloading,album_downloading),
                                       (self.downloaded, album_downloaded),
                                       (self.tags, album_tags),
                                       (self.cover, album_cover),
                                       (self.replay_gain, album_replay_gain),
                                       (self.server_upload, album_server_upload)]:
            check_value.trace_add('write', self.change_checkbox_colour(check_value, check_box))

            # Update the colours of values are loaded

            if check_value.get():
                check_box.config(bg="green", activebackground="red")
            else:
                check_box.config(bg="red", activebackground="green")

    @staticmethod
    def change_checkbox_colour(value: tk.BooleanVar, button: tk.Checkbutton):
        """
        This function returns a function so the checkboxes can have their colours turned from red to green
        depending on their values
        :param value: The Variable the checkbox is attached to
        :param button: The actual checkbox
        :return: Function to change colour
        """
        def change_colour(*_):
            if value.get():
                button.config(bg="green", activebackground="green")
            else:
                button.config(bg="red", activebackground="red")

        return change_colour


    def delete_album(self):
        """
        This function deletes the album from the selected Artists album list and removes the frame from
        the album screen
        """
        self.selected_artist.delete_album(self.original_title)
        self.frame.destroy()

        # Had to write a loop because self.album_frame_list.remove(self.album_frame) did not work

        for album_frame in self.album_frame_list:
            if album_frame.original_title == self.original_title:
                self.album_frame_list.remove(album_frame)


class NewAlbumFrame:

    def __init__(self, parent_frame, album_data_parent_frame, album_frames_list:list[AlbumDataFrame],
                 send_response_message):
        """
        A NewAlbumFrame is an empty frame that allows new Album objects to be added to an Artist and to
        the list of Albums in the DataEditingPanel. It allows the Title, Type, Year, Downloading Status, Markers,
        and Notes to be prefilled.
        :param parent_frame: The root object that the list of Albums will be displayed in
        """

        self.send_response_message = send_response_message
        self.selected_artist = None
        self.album_frames_list = album_frames_list
        self.album_data_parent_frame = album_data_parent_frame

        self.frame = tk.Frame(parent_frame)
        self.frame.pack(side="bottom")
        tk.Label(self.frame, text="Add New Album:").pack(side="left")

        # Make variables

        self.title = tk.StringVar()
        self.type = tk.StringVar(value="studio_album")
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
        """
        This function adds a new album using data filled out in the Entry boxes.
        This function creates the Album object, makes a new AlbumDataFrame and adds the Album to the Artist
        """

        if self.selected_artist is None:
            self.send_response_message("You have not selected an artist!")
            return

        if self.title.get().strip() == "":
            self.send_response_message("No title selected")

        if not self.year.get().isdigit():
            self.send_response_message("Date is invalid!")
            return

        artist_album_list = []

        for album in self.selected_artist.albums:
            artist_album_list.append(album.title.lower())

        if self.title.get().strip().lower() in artist_album_list:
            self.send_response_message("Album already exists")
            return

        new_album = Album(self.title.get().strip(), self.type.get(), int(self.year.get()), self.downloading.get(),
                          markers=self.markers.get(), notes=self.notes.get())

        self.selected_artist.albums.append(new_album)
        new_frame = AlbumDataFrame(self.album_data_parent_frame, new_album, self.selected_artist, self.album_frames_list)
        self.album_frames_list.append(new_frame)

        self.title.set("")
        self.year.set("")
        self.downloading.set(False)
        self.markers.set("")
        self.notes.set("")


class DataEditingPanel:
    """
    This class is the right side of the editing screen. Along the top it has the Artist information that
    can be edited. Below the Artist information is the list of Albums belonging to that Artist. These can
    also be modified.
    """
    # todo add a status to show whether changes are saved to database


    def __init__(self, window:tk.Tk, artist_storage:ArtistStorage):
        """
        This function creates the DataEditingPanel, that is displayed on the right-hand side of the manual
        editing screen. This does not take an Artist value as the Artist is updated later.
        :param window: The editing screen
        """
        self.artist_storage = artist_storage

        self.selected_artist = None
        self.album_frames = []
        data_editor = tk.Frame(window)
        data_editor.pack(side="right", expand=True, padx=10, pady=(10, 10))

        # Add new artist

        new_artist_frame = tk.Frame(data_editor)
        new_artist_frame.pack(side="top")

        self.new_artist_name = tk.StringVar(value="")
        tk.Entry(new_artist_frame, textvariable=self.new_artist_name).pack(side="left")
        tk.Button(new_artist_frame, text="Add Artist", command=self.add_new_artist).pack(side="left")

        # Save button and response box

        save_response_frame = tk.Frame(data_editor)
        save_response_frame.pack(side="top")

        save_button = tk.Button(save_response_frame, text="Write to Database", command=self.update_artist_data)
        save_button.pack(side="left")

        self.response_box = tk.Text(save_response_frame, state="disabled", height=1, width=100)
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
        tk.Button(artist_information, text="Delete Artist", command=self.delete_artist).pack(side="left")

        # Album Editor

        self.album_editor = tk.Frame(data_editor, background="#e8cc2a", padx=10, pady=10)
        self.album_editor.pack(side="top", fill="both", expand=True)

        tk.Label(self.album_editor, text="Albums: ").pack(side="top", anchor="nw")

        self.new_album_creator = NewAlbumFrame(data_editor, self.album_editor, self.album_frames,
                                               self.send_response_message)


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

        for album_frame in  self.album_frames: # Get each album displayed in the editing panel
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


    def delete_artist(self):
        self.artist_storage.delete_artist(self.selected_artist)

        # todo, clear out artist data
        # todo, reload the artist_list

        self.send_response_message("Deleted artist")


    def add_new_artist(self):
        # Make sure an Artist with the same name does not already exist

        existing_artists = [name.lower() for name in self.artist_storage.get_selectable_artists()]
        new_artist_name = self.new_artist_name.get().strip() # todo, could some of the .strip() stuff be run in the artist constructor?

        if new_artist_name.lower() in existing_artists:
            self.send_response_message("Artist already exists")
            return

        self.artist_storage.create_artist(new_artist_name)

        self.set_selected_artist(new_artist_name)
        self.send_response_message("New artist has been created")


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
        self.selected_artist = self.artist_storage.get_artist(selected_artist_name)

        # Set the Entry box variables to artist data

        self.name.set(self.selected_artist.name)
        if self.selected_artist.markers is not None:
            self.markers.set(self.selected_artist.markers)
        if self.selected_artist.notes is not None:
            self.notes.set(self.selected_artist.notes)

        # Create an AlbumFrame for each Album and put it in the editor

        for album in self.selected_artist.albums:
            frame = AlbumDataFrame(self.album_editor, album, self.selected_artist, self.album_frames)
            self.album_frames.append(frame)

        self.new_album_creator.selected_artist = self.selected_artist

        self.send_response_message(f"Selected artist: {self.selected_artist.name}")

