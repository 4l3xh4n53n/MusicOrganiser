import tkinter as tk

from openpyxl import load_workbook

import database


def create_window():
    window = tk.Tk()
    title = tk.Label(text="Music Organiza!")
    title.pack()

    # What do I need besides a title???

    # Option to select artist and create folders for what is missing!

    # Input directory
    # directory search window?

    # Album name
    # Album date
    # Artist name
    # Show different for CD1 and CD2

    # List track numbers, track names, and file names

    # Onto the automation stuff

    # Automatically create folders of what is missing but downloaded (taken from database)

    # A thing to add a new artist and add a wanted album (can set with album, ep, compilation, single, etc)

    window.mainloop()

if __name__ == "__main__":
    #create_window()

    # TODO, make the album thing into a Tuple of (name, date), or every better, make a data structure
    database.add_artist("Anthrax")
    database.add_artist("System of a Down")
    database.add_artist("Meshuggah")
    database.add_artist("Dream Theater")
    database.add_artist("TOOL")

    workbook = load_workbook("test.xlsx")
    sheet = workbook.active
    result = database.find_artist(sheet, "Meshuggah")
    print(result)
