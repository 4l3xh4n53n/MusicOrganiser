from src.data.album import Album

import tkinter as tk

from src.data.artist import Artist


def make_window(artist:Artist, album:Album):
    """
    This window is made up of 3 smaller windows, 1 for tagging, 1 for covers, and another for
    ReplayGain, format conversion
    """
    window = tk.Tk()
    window.maxsize(2000, 1000)
    window.geometry("1800x950")

    # todo, call upon other windows here

    tk.mainloop()

