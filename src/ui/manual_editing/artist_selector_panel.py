import tkinter as tk
from tkinter import SINGLE

from src.data.database import filter_artist_list, get_artist_list
from src.ui.manual_editing.data_editing_panel import DataEditingPanel


class ArtistSelectorPanel:
    """
    This class is the left side of the editing screen. It has three boxes, a search box, a list of Artists
    and a bookmarks box at the bottom to make it easier to switch back and forth between Artists. Once an
    Artist has been selected it calls the set_selected_artist() function from the DataEditingPanel class.
    """


    def __init__(self, window:tk.Tk, data_editing_panel: DataEditingPanel):
        """
        This function creates the ArtistSelectorPanel that is displayed on the left-hand side of the manual
        editing screen. It allows an Artist to be selected and bookmarked.
        :param window: The root window that the artist selector will go in
        :param data_editing_panel: The DataEditingPanel that it will update when an Artist is chosen
        """
        self.data_editing_panel = data_editing_panel

        # Make a frame to contain the selection panel elements

        artist_selector = tk.Frame(window)
        artist_selector.pack(side="left", expand=True, padx=10, pady=(10, 10))

        # Create the window elements

        artist_search_box = tk.Entry(artist_selector, width=52)
        self.artist_list_box = tk.Listbox(artist_selector, height=34, width=52, selectmode=SINGLE)
        self.bookmarked_artists = tk.Listbox(artist_selector, height=10, width=52, selectmode=SINGLE)

        artist_search_box.bind("<Return>", lambda event: self.filter_artist_list(event))

        # Select Artist

        self.artist_list_box.bind("<Double-1>", lambda event: self.select_artist(event))
        self.bookmarked_artists.bind("<Double-1>", lambda event: self.select_artist(event))

        # Bookmarks

        self.artist_list_box.bind("<Button-3>", lambda event: self.bookmark_artist(event))
        self.bookmarked_artists.bind("<Button-3>", lambda event: self.remove_artist_from_bookmarks(event))

        # Pack all items

        artist_search_box.pack()
        self.artist_list_box.pack()
        self.bookmarked_artists.pack()

        self.set_artist_list_box_contents(get_artist_list())


    def filter_artist_list(self, event):
        """
        This function takes the value in the search box and filters the artist name list.
        :param event: Enter button event
        """
        search_query = event.widget.get()
        artist_list = filter_artist_list(search_query)
        self.set_artist_list_box_contents(artist_list)


    def set_artist_list_box_contents(self, artist_list: list[str]):
        """
        Changes the displayed list of Artists.
        :param artist_list: List of Artists to be displayed in the listbox.
        """
        self.artist_list_box.delete(0, tk.END)
        for item in artist_list:
            self.artist_list_box.insert(tk.END, item)


    def bookmark_artist(self, event):
        """
        This function adds an Artist to the bookmarked section of the selection panel.
        :param event: The event (this finds the selected artist)
        """
        selected_index = self.artist_list_box.nearest(event.y)
        selected_artist = self.artist_list_box.get(selected_index)

        if selected_artist in self.bookmarked_artists.get(0, tk.END): # Check artist isn't already bookmarked
            return

        self.bookmarked_artists.insert(tk.END, selected_artist)


    def remove_artist_from_bookmarks(self, event):
        """
        This function removes an Artist from the bookmarked section of the selection panel.
        :param event: The event (this finds the selected artist)
        """
        selected_index = self.bookmarked_artists.nearest(event.y)
        if selected_index != (): # Ensure an artist has been selected
            self.bookmarked_artists.delete(selected_index, selected_index)


    def select_artist(self, event):
        """
        This function selects an artist for their data to be populated in the data editing panel.
        :param event: The event ( this finds the selected artist)
        """
        listbox = event.widget
        selected_index = listbox.nearest(event.y)
        selected_artist = listbox.get(selected_index)
        self.data_editing_panel.set_selected_artist(selected_artist)

