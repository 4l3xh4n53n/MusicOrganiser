import tkinter as tk
from copy import deepcopy

from src.data.album import Album
from src.data.artist import Artist
from src.data.artist_storage import ArtistStorage


class DataFrame:
    """
    This class stores data relating to new or existing albums. It can be used from NewAlbumFrame or an AlbumDataFrame
    """

    def __init__(self, parent_frame, boxes):
        """
        This function takes a list of tuples each containing 4 items, their order depending on the type of variable.
        The format for boxes is simple.

        - Variable Name - This is quite simply the name of the variable in the class
        - Box Type - This is the type of input box that is used in the tkinter UI
        - Special - This one depends on the input box type:
            - Entries - This defines how wide the Entry box will be
            - OptionMenus - This defines the selectable options
            - Checkbuttons - This defines the label for the Checkbutton
        - Variable - This is the variable that the box will be linked to

        :param parent_frame: This is the frame that the DataFrame is being packed into
        :param boxes: This is where the variables for each frame are stored
        """

        for variable_name, box_type, special, variable in boxes:
            new_box = None

            if box_type is tk.Entry:
                new_variable = tk.StringVar(value=variable)
                setattr(self, variable_name, new_variable)
                new_box = tk.Entry(parent_frame, width=special, textvariable=new_variable)

            if box_type is tk.OptionMenu:
                new_variable = tk.StringVar(value=variable)
                setattr(self, variable_name, new_variable)
                new_box = tk.OptionMenu(parent_frame, new_variable, *special)

            if box_type is tk.Checkbutton:
                new_variable = tk.BooleanVar(value=variable)
                setattr(self, variable_name, new_variable)
                new_box = tk.Checkbutton(parent_frame, text=special, height=1, variable=new_variable)

                # Make the checkbox colour changed based on whether its value is True or False

                new_variable.trace_add('write', self.change_checkbox_colour(new_variable, new_box))
                if variable is True:
                    new_box.config(bg="green", activebackground="red")
                else:
                    new_box.config(bg="red", activebackground="green")

            new_box.pack(side="left")


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

        self.original_title = album.title
        self.selected_artist = selected_artist
        self.album_frame_list = album_frame_list

        # Make a frame for the album

        self.frame = tk.Frame(parent_frame)
        self.frame.pack()

        boxes = [
            ('title', tk.Entry, 30, album.title),
            ('type', tk.OptionMenu, ["studio_album", "ep", "compilations", "covers", "singles"], album.type),
            ('date', tk.Entry, 6, str(album.date)),

            ('downloading', tk.Checkbutton, "Downloading", album.downloading),
            ('downloaded', tk.Checkbutton, "Downloaded", album.downloaded),
            ('tags', tk.Checkbutton, "Tags", album.tags),
            ('cover', tk.Checkbutton, "Cover", album.cover),
            ('replay_gain', tk.Checkbutton, "Replay Gain", album.replay_gain),
            ('server_upload', tk.Checkbutton, "Server Upload", album.server_upload),

            ('format', tk.Entry, 8, album.format),
            ('markers', tk.Entry, 6, album.markers if album.markers is not None else ""),
            ('notes', tk.Entry, 40, album.notes if album.notes is not None else "")
        ]

        self.data = DataFrame(self.frame, boxes)

        # Make delete button

        delete_button = tk.Button(self.frame, text="Delete", command=self.delete_album)
        delete_button.pack(side="left")


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
        the list of Albums in the DataEditingPanel. It allows the Title, Type, Date, Downloading Status, Markers,
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

        boxes = [
            ('title', tk.Entry, 30, ""),
            ('type', tk.OptionMenu, ["studio_album", "ep", "compilations", "covers", "singles"], "studio_album"),
            ('date', tk.Entry, 6, ""),
            ('downloading', tk.Checkbutton, "Downloading", False),
            ('markers', tk.Entry, 6, ""),
            ('notes', tk.Entry, 40, "")
        ]

        self.data = DataFrame(self.frame, boxes)

        # Save new album box

        tk.Button(self.frame, text="Save", command=self.add_new_album).pack(side="left")


    def add_new_album(self):
        """
        This function adds a new album using data filled out in the Entry boxes.
        This function creates the Album object, makes a new AlbumDataFrame and adds the Album to the Artist
        """

        if self.selected_artist is None:
            self.send_response_message("You have not selected an artist!")
            return

        if self.data.title.get().strip() == "":
            self.send_response_message("No title selected")

        if not self.data.date.get().isdigit():
            self.send_response_message("Date is invalid!")
            return

        artist_album_list = []

        for album in self.selected_artist.albums:
            artist_album_list.append(album.title.lower())

        if self.data.title.get().strip().lower() in artist_album_list:
            self.send_response_message("Album already exists")
            return

        new_album = Album(self.data.title.get().strip(), self.data.type.get(), int(self.data.date.get()),
                          self.data.downloading.get(), markers=self.data.markers.get(), notes=self.data.notes.get())

        self.selected_artist.albums.append(new_album)
        new_frame = AlbumDataFrame(self.album_data_parent_frame, new_album, self.selected_artist, self.album_frames_list)
        self.album_frames_list.append(new_frame)

        self.data.title.set("")
        self.data.date.set("")
        self.data.downloading.set(False)
        self.data.markers.set("")
        self.data.notes.set("")


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

            album.title = album_frame.data.title.get().strip() # todo, make sure this title doesn't exist anywhere else!
            album.type = album_frame.data.type.get().strip()
            album.type = album_frame.data.type.get().strip()
            if album_frame.data.date.get().isdigit():
                album.date = int(album_frame.data.date.get())
            else:
                self.send_response_message("Date format is not valid")
                return

            album.downloading = album_frame.data.downloading.get() # todo soon we will loop through all album_frame.data variables
            album.downloaded = album_frame.data.downloaded.get()
            album.tags = album_frame.data.tags.get()
            album.cover = album_frame.data.cover.get()
            album.replay_gain = album_frame.data.replay_gain.get()
            album.server_upload = album_frame.data.server_upload.get()

            album.format = album_frame.data.format.get()
            album.markers = album_frame.data.markers.get().strip()
            album.notes = album_frame.data.notes.get().strip()

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

