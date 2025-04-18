"""
This file handles the database. The database used is a xlsx file.
"""

from openpyxl.reader.excel import load_workbook
from openpyxl.styles import Alignment, PatternFill

"""
Markers:
I might change these to priorities!

Markers for artists:
G = get something
F = finish discography

Markers for albums:
G = get this album
"""

# This function returns the albums for an artist
def get_artist(artist_name):
    workbook = load_workbook("test.xlsx")
    sheet = workbook.active

    sheet["A1"] = "|"
    sheet["B1"] = "||"
    sheet["A2"] = "||"
    sheet["B2"] = "|_"

    sheet.insert_rows(0, 2)

    workbook.save(filename="test.xlsx")

    print("Getting Artist!")


def add_artist(artist, albums):

    def insert_empty_rows():
        sheet.insert_rows(previous_artist_position, 1 + len(albums))

    """
    This function un-merges and re-merges cells in order to keep the formatting of the 
    spreadsheet when new rows are inserted for storing new artists and/or albums.
    
    For reference:
    - Artist cells, span columns A to I and are the name of the artist all albums are found under
    their background colour is: #B4C7DC
    - Album type cells, span columns A to C and differentiates different types of albums, such as 
    compilation, EP, Studio, etc... 
    their background colour is: #FF972F
    """
    def format_cells():

        # TODO, add formatting for headings like singles and compilations as these have separate rules
        # todo this I would have to add albums, singles, compilations, ep's as multiple separate thingies (I may handle this elsewhere in the code)

        # Create a copy to stop iteration error
        merged_cells = list(sheet.merged_cells)

        # Un-merge cells

        for merged_cell_range in merged_cells:
            merged_row = merged_cell_range.min_row
            if merged_row > new_artist_position:
                # For some reason which I cannot figure out, sheet.unmerge_cells always complains it
                # cannot find the cells to unmerge and the code "fails" however, the cells are still un-merged
                #  without this code the cells remain merged
                try:
                    sheet.unmerge_cells(range_string="A" + str(merged_row) + ":I" + str(merged_row))
                except KeyError:
                    pass

        # Re-merge cells

        for merged_cell_range in merged_cells:
            merged_row = merged_cell_range.min_row
            if merged_row >= new_artist_position:
                new_cell_row = str(merged_cell_range.min_row + 1 + len(albums))

                # Cell is an artist cell
                if row[0].fill == PatternFill("solid", fgColor="B4C7DC"):
                    sheet.merge_cells("A" + new_cell_row + ":I" + new_cell_row)

                # Cell is an album type cell
                else:
                    sheet.merge_cells("A" + new_cell_row + ":C" + new_cell_row)

    workbook = load_workbook("test.xlsx")
    sheet = workbook.active

    # Find out where in the spreadsheet the artist should be positioned

    previous_artist_position = 1

    for row_index, row in enumerate(sheet.iter_rows(min_row=1), start=1):

        # If the end of the spreadsheet has been reached
        if row[0].value is None:
            previous_artist_position = row_index
            insert_empty_rows()
            break

        # Figure out if the cell contains an artists name by its background colour
        if row[0].fill == PatternFill("solid", fgColor="B4C7DC"):

            # The new artist (alphabetically) comes before this artist (found position and finish loop)
            if artist < row[0].value:
                previous_artist_position = row_index
                insert_empty_rows()
                break

            # The new artist (alphabetically) comes after this artist (continue loop)
            else:
                previous_artist_position = row_index

    new_artist_position = previous_artist_position

    format_cells()

    # Merges new cell and sets content and formatting
    sheet.merge_cells("A" + str(new_artist_position) + ":I" + str(new_artist_position))
    sheet["A" + str(new_artist_position)] = artist
    sheet["A" + str(new_artist_position)].alignment = Alignment(horizontal="center")
    sheet["A" + str(new_artist_position)].fill = PatternFill("solid", fgColor="B4C7DC")

    # Add each of the albums under the artist

    for album_index, album in enumerate(albums, start=1):
        album_position = str(new_artist_position + album_index)
        sheet["A" + album_position] = album[0]
        sheet["B" + album_position] = album[1]

    workbook.save("test.xlsx")
