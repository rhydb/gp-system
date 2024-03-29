from tkinter import *
from ScrolledFrame import *
'''
the tables class allows for creating a table with a set row and column count as well as add headers and specific widths
it does this by creating multiple entry boxes and gridding them
'''
class Table(Frame):
    def __init__(self, parent, *args, rows=1, columns=1, show_headers=False, headers: list = [], widths=[], **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        self.widths = [10] * columns # default width of 10
        if widths:
            # if widths was entered check if it was an int or a list
            # if it was an int create a list of the width as many times as there are column
            if type(widths) is int:
                self.widths = [widths] * columns
            elif type(widths) is list:
                for i in range(len(widths)):
                    self.widths[i] = widths[i] # set the widths to the new widths 
            else:
                raise Exception(f"Invalid type for widths '{type(widths)}' expted int or list") # the widths was an invalid type

        if show_headers is True:
            # handle any errors with the headers
            if not headers:
                raise Exception(f"No headers provided, even though show_headers is set to True")
            if len(headers) != columns:
                raise Exception(f"Number of headers ({len(headers)}) must be equal to nmber of columns ({columns})")
            if len(headers) != len(set(headers)):
                raise Exception(f"Header list contains duplicates")

        self.table = [] # the list of the actual entry boxes
        self.headers = headers
        self.show_headers = show_headers
        self.rows = rows
        self.columns = columns

        for i in range(rows):
            self.table.append([])
            for j in range(columns):
                self.table[i].append(Entry(self, width=self.widths[j])) # make the entry boxes and add them into the list

    def grid_headers(self): # method to add all the headers at the right place
        for i in range(len(self.headers)):
            Label(self, text=self.headers[i]).grid(row=0, column=i)

    def grid_cells(self):
        for i in range(self.rows):
            for j in range(self.columns):
                self.table[i][j].grid(row=i + (1 if self.headers else 0), column=j) # add all the entry boxes into the right place

    def grid(self, *args, **kwargs): # grid everything together
        if self.show_headers:
            self.grid_headers()
        self.grid_cells()
        Frame.grid(self, *args, **kwargs) # grid the frame

    def pack(self, *args, **kwargs):
        if self.show_headers:
            self.grid_headers()
        self.grid_cells()
        Frame.pack(self, *args, **kwargs) # grid everything then pack the frame
    def get_header_index(self, header):
            return self.headers.index(header) # return the index of the header using the value
    def get_row(self, row: int):
        return [cell.get() for cell in self.table[row]] # return a specific row as a list
    def get_column(self, column): # return a specific column as a list
        if type(column) is str:
            column = self.get_header_index(column)
        elif type(column) is not int:
            raise Exception(f"Invalid type for column '{type(column)}'")
        return [row[column].get() for row in self.table]

    def get_cell(self, column: int = 0, row: int = 0): # get a specific cells value
        return self.table[column][row].get()

    def set_cell(self, row: int, column: int, value: str): # method to set a specific cell's value
        self.table[row][column].delete(0,END)
        self.table[row][column].insert(0,str(value))

    def set_column(self, column, value): # set an entire column to a specific value or set of values
        if type(column) is str:
            column = self.get_header_index(column)
        elif type(column) is not int:
            raise Exception(f"Invalid type for column '{type(column)}'")
        if type(value) is list:
            if len(value) != self.rows:
                raise Exception(f"Invalid number of items to set column {len(value)}/{self.rows}")
            for j, item in enumerate(value): # set all the cells to the value in the list 
                self.set_cell(j, column, item)
        else:
            for i in range(self.rows): # set all the cells to the one value
                self.set_cell(i, column, value)

    def set_row(self, row_index, row_values): # set an entire row to a set of values
        for i in range(min(len(row_values), self.columns)): # use either the length of values or the number of columns if there are too many values
            # go through each column and set the specified row's entry box
            # to the corresponding value
            self.set_cell(row_index, i, row_values[i])
    def add_row(self): # append a new row to the table full of empty entry boxes with the correct widths
        self.table.append([])
        self.rows += 1
        for i in range(self.columns):
            self.table[-1].append(Entry(self, width=self.widths[i])) # add an entry to the last row
            self.table[-1][-1].grid(row=self.rows + (1 if self.headers else 0), column=i) # grid the new entry

    def set_row_count(self, row_count):
        if (row_count < self.rows):
            # remove rows
            for i in range(self.rows - row_count):
                # go through every row and remove the last item until the row count is right
                for entry in self.table[-1]:
                    entry.destroy() # remove the entry from the screen
                self.table.pop() # remove the entire row from the list
        else:
            # add rows
            for _ in range(row_count - self.rows): # add the extra rows
                self.add_row()
        self.rows = row_count # update the row count
