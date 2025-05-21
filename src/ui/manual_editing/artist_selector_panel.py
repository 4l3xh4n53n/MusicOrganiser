import tkinter as tk
from tkinter import SINGLE

from src.data.database import filter_artist_list, get_artist_list
from src.ui.manual_editing.data_editing_panel import DataEditingPanel


class ArtistSelectorPanel:

    selected_artist = ""

    def __init__(self, window:tk.Tk, data_editing_panel: DataEditingPanel):
        self.data_editing_panel = data_editing_panel

        # Make a frame to contain the selection panel elements

        artist_selector = tk.Frame(window)
        artist_selector.pack(side="left", expand=True, padx=10, pady=(10, 10))

        # Create the window elements

        artist_search_box = tk.Entry(artist_selector, width=52)
        list_of_artists = tk.Listbox(artist_selector, height=34, width=52, selectmode=SINGLE)
        self.bookmarked_artists = tk.Listbox(artist_selector, height=10, width=52, selectmode=SINGLE)

        artist_search_box.bind("<Return>", lambda event: self.artist_search(event, list_of_artists))

        # Select Artist

        list_of_artists.bind("<Double-1>", lambda event: self.select_artist(event))
        self.bookmarked_artists.bind("<Double-1>", lambda event: self.select_artist(event))

        # Bookmarks

        list_of_artists.bind("<Button-3>", lambda event: self.bookmark_artist(event))
        self.bookmarked_artists.bind("<Button-3>", lambda event: self.remove_artist_from_bookmarks(event))

        # Pack all items

        artist_search_box.pack()
        list_of_artists.pack()
        self.bookmarked_artists.pack()

        self.set_list_box_contents(list_of_artists, get_artist_list())


    def artist_search(self, event, list_of_artists):
        search_query = event.widget.get()
        artist_list = filter_artist_list(search_query)
        self.set_list_box_contents(list_of_artists, artist_list)


    @staticmethod
    def set_list_box_contents(listbox: tk.Listbox, artist_list):
        listbox.delete(0, tk.END)
        for item in artist_list:
            listbox.insert(tk.END, item)


    def bookmark_artist(self, event):
        list_of_artists = event.widget

        selected_index = list_of_artists.nearest(event.y)
        selected_artist = list_of_artists.get(selected_index)

        if selected_artist in self.bookmarked_artists.get(0, tk.END): # Check artist isn't already bookmarked
            return

        self.bookmarked_artists.insert(tk.END, selected_artist)


    def remove_artist_from_bookmarks(self, event):

        selected_index = self.bookmarked_artists.nearest(event.y)
        if selected_index != (): # Ensure an artist has been selected
            self.bookmarked_artists.delete(selected_index, selected_index)


    def select_artist(self, event):
        listbox = event.widget
        selected_index = listbox.nearest(event.y)
        self.selected_artist = listbox.get(selected_index)
        self.data_editing_panel.set_selected_artist(self.selected_artist)

