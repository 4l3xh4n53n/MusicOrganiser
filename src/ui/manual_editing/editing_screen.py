import tkinter as tk

from src.ui.manual_editing.artist_selector_panel import ArtistSelectorPanel
from src.ui.manual_editing.data_editing_panel import DataEditingPanel


def create_window():
    window = tk.Tk()
    window.maxsize(2000,1000)
    window.geometry("1800x950")

    editing_panel = DataEditingPanel(window)
    ArtistSelectorPanel(window, editing_panel)

    tk.mainloop()

