import tkinter as tk
from tkinter import SINGLE

from src.data.database import filter_artist_list, get_artist_list


def artist_search(event, list_of_artists):
    search_query = event.widget.get()
    artist_list = filter_artist_list(search_query)
    set_list_box_contents(list_of_artists, artist_list)


def set_list_box_contents(listbox: tk.Listbox, artist_list):
    listbox.delete(0, tk.END)
    for item in artist_list:
        listbox.insert(tk.END, item)


def bookmark_artist(event, bookmarked_artists):
    list_of_artists = event.widget

    selected_index = list_of_artists.nearest(event.y)
    selected_artist = list_of_artists.get(selected_index)

    if selected_artist in bookmarked_artists.get(0, tk.END): # Check artist isn't already bookmarked
        return

    bookmarked_artists.insert(tk.END, selected_artist)


def remove_artist_from_bookmarks(event):
    bookmarked_artists = event.widget

    selected_index = bookmarked_artists.nearest(event.y)
    if selected_index != (): # Ensure an artist has been selected
        bookmarked_artists.delete(selected_index, selected_index)


def select_artist(event):
    listbox = event.widget
    selected_index = listbox.nearest(event.y)
    selected_artist = listbox.get(selected_index)
    print(selected_artist) # todo, not sure what to do from here
    # do we set it as a global variable here>
    # or do we call the other side of the screen?
    # Probably the latter


def create_panel(window:tk.Tk):
    # Make a frame to contain the selection panel elements

    artist_selector = tk.Frame(window)
    artist_selector.pack(side="left", expand=True, padx=10, pady=(10, 10))

    # Create the window elements

    artist_search_box = tk.Entry(artist_selector, width=52)
    list_of_artists = tk.Listbox(artist_selector, height=34, width=52, selectmode=SINGLE)
    bookmarked_artists = tk.Listbox(artist_selector, height=10, width=52, selectmode=SINGLE)

    artist_search_box.bind("<Return>", lambda event: artist_search(event, list_of_artists))

    # Select Artist

    list_of_artists.bind("<Double-1>", lambda event: select_artist(event))
    bookmarked_artists.bind("<Double-1>", lambda event: select_artist(event))

    # Bookmarks

    list_of_artists.bind("<Button-3>", lambda event: bookmark_artist(event, bookmarked_artists))
    bookmarked_artists.bind("<Button-3>", lambda event: remove_artist_from_bookmarks(event))

    # Pack all items

    artist_search_box.pack()
    list_of_artists.pack()
    bookmarked_artists.pack()

    set_list_box_contents(list_of_artists, get_artist_list())