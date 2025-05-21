import tkinter as tk

from src.ui.manual_editing import data_editing_panel
from src.ui.manual_editing.artist_selector_panel import ArtistSelectorPanel


def create_window():
    window = tk.Tk()
    window.maxsize(2000,1000)
    window.geometry("1800x950")

    artist_selector = ArtistSelectorPanel(window)

    tk.mainloop()

