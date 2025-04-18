import tkinter as tk

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

    # TODO, make the album thing into a Tuple of (name, date)
    database.add_artist("Rammstein", [("Herzeleid", "1984"), ("Sehnsucht", "1984")])
    database.add_artist("System of a Down", [("System of a Down", "1998"), ("Toxicity", "2001"), ("Steal This Album", "2002"), ("Mesmerize", "2005"), ("Hypnotize", "2005")])
    database.add_artist("Anthrax", [("Fistful of metal", "1984"), ("Spreading The Disease", "1984"), ("Among The Living", "1984")])

