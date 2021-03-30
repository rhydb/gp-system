from tkinter import *
from ScrolledFrame import *

class Table(Frame):
    def __init__(self, parent, *args, rows=1, columns=1, show_headers=False, headers: list = [], widths=[], **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        if not widths:
            widths = [10] * (columns-1)
        elif type(widths) is int:
            widths = [widths] * columns
        self.widths = widths
        if show_headers is True:
            if not headers:
                raise Exception(f"No headers provided, even though show_headers is set to True")
            if len(headers) != columns:
                raise Exception(f"Number of headers ({len(headers)}) must be equal to nmber of columns ({columns})")
            if len(headers) != len(set(headers)):
                raise Exception(f"Header list contains duplicates")

        self.table = []
        self.headers = headers
        self.show_headers = show_headers
        self.rows = rows
        self.columns = columns
        for i in range(columns):
            self.table.append([])
            for j in range(rows):
                self.table[i].append(Entry(self, width=self.widths[j]))

    def grid_headers(self):
        for i in range(len(self.headers)):
            Label(self, text=self.headers[i]).grid(row=0, column=i)

    def grid_cells(self):
        for i in range(self.columns):
            for j in range(self.rows):
                self.table[i][j].grid(row=j + (1 if self.headers else 0), column=i)

    def grid(self, *args, **kwargs):
        if self.show_headers:
            self.grid_headers()
        self.grid_cells()
        Frame.grid(self, *args, **kwargs)

    def pack(self, *args, **kwargs):
        if self.show_headers:
            self.grid_headers()
        self.grid_cells()
        Frame.pack(self, *args, **kwargs)
    def get_header_index(self, header):
            return self.headers.index(header)
    def get_row(self, row: int):
        return [column[row].get() for column in self.table]
    def get_column(self, column):
        if type(column) is str:
            column = self.get_header_index(column)
        elif type(column) is not int:
            raise Exception(f"Invalid type for column '{type(column)}'")
        return [cell.get() for cell in self.table[column]]

    def get_cell(self, column: int = 0, row: int = 0):
        return self.table[column][row].get()

    def set_cell(self, column: int, row: int, value: str):
        self.table[column][row].delete(0,END)
        self.table[column][row].insert(0,str(value))

    def set_column(self, column, value):
        if type(column) is str:
            column = self.get_header_index(column)
        elif type(column) is not int:
            raise Exception(f"Invalid type for column '{type(column)}'")
        if type(value) is list:
            if len(value) != self.rows:
                raise Exception(f"Invalid number of items to set column {len(value)}/{self.rows}")
            for i in range(self.rows):
                self.set_cell(column, i, value[i])
        else:
            for i in range(self.rows):
                self.set_cell(column, i, value)
    def set_row(self, row_index, row_values):
        for i in range(len(row_values)):
            # go through each column and set the specified row's entry box
            # to the corresponding value
            self.set_cell(i, row_index, row_values[i])
    def add_row(self):
        for i in range(self.columns):
            self.table[i].append(Entry(self))
            self.table[i][self.rows].grid(row=self.rows + (1 if self.headers else 0), column=i)
        self.rows += 1
    def set_row_count(self, row_count):
        if (row_count < self.rows):
            # remove rows
            for i in range(self.rows - row_count):
                # go through every column and remove the last item until the row count is right
                for j in range(self.columns):
                    self.table[j][-1].destroy() # destroy the entry box to remove it from the screen
                    self.table[j].pop() # remove the entry box from the list
        else:
            # add rows
            for _ in range(row_count - self.rows): # add the extra rows
                self.add_row()
        self.rows = row_count # update the row count
