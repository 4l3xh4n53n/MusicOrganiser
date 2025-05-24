import tkinter as tk

from src.ui.manual_editing.artist_selector_panel import ArtistSelectorPanel
from src.ui.manual_editing.data_editing_panel import DataEditingPanel


def create_window():
    """
    This creates the window that allows you to manually edit Artist and Album data.
    This window is made from two separate tkinter frames, one that handles searching
    for and selecting an Artist, the other for modifying the Artist and Album data.
    """
    window = tk.Tk()
    window.maxsize(2000,1000)
    window.geometry("1800x950")

    # This is the right side of the window
    editing_panel = DataEditingPanel(window)
    # This is the left side of the window
    ArtistSelectorPanel(window, editing_panel)

    tk.mainloop()

