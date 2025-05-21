import tkinter as tk
from tkinter.constants import SINGLE

from src.data.database import filter_artist_list, get_artist_list
from src.ui.manual_editing import artist_selector_panel


def create_window():
    window = tk.Tk()
    window.maxsize(2000,1000)
    window.geometry("1800x950")

    artist_selector_panel.create_panel(window)

    tk.mainloop()

