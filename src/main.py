import tkinter as tk

"""
Regarding Notes:
Put simply, they are notes, you can write anything you want
Regarding Markers:
These markers mean there is an issue with something
D - Date
N - Name
C - Cover
A - Album
B - Artist 

These markers show intentions or improvements:
G - Get this album/artist
F - Finish this discography
E - Download included extra content that is worth checking out
"""

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
    create_window()


