from tkinter import *

'''
a class that can create different widgets by using a dicitonairy
this is used throughout the program and the forms are defined in the database handler
the dictionairies allow for easy to create and edit forms that are more readable than python code

it also allows for checking if all the required items have been entered
'''
class Form(Frame):
    def __init__(self, parent, *args, data=[], display="block", **kwargs):
        Frame.__init__(self, parent, *args, *kwargs)
        self.data = data
        self.form_items = {} # this will contain each item's name and a stringvar to hold its content
        if display != "block" and display != "inline":
            raise Exception(f"Display must be 'block' or 'inline' not '{display}'")

        for j, item in enumerate(data): # data is an array of dictionaries
            # go through each item and build the correct widget
            self.form_items[item.get("name")] = StringVar()
            Label(self, text=item.get("display_name") + ("*" if item.get("required") else " ")).grid(row=(j if display == "block" else 0), column=(0 if display == "block" else j))
            if item.get("type") == "entry": # check what type of widget it is and create the appropiate type
                Entry(self, textvar=self.form_items[item.get("name")]).grid(row=(j if display == "block" else 1), column=(1 if display == "block" else j))
            elif item.get("type") == "dropdown":
                OptionMenu(self, self.form_items[item.get("name")], *item.get("menu_items")).grid(row=(j if display == "block" else 1), column=(1 if display == "block" else j))

    def completed_required(self): # check if all required items have been entered
        for item in self.data:
            if item.get("required") and not self.form_items[item["name"]].get():
                return False
        return True
    def get(self, name):
        return self.form_items.get(name).get() # return the given item's content
    def get_all(self, allow_empty=True):
        return [item.get() for item in self.form_items.values() if allow_empty is True or item.get()] # make a list out of all the items' stringvar's
    def set_all(self, data):
        for j, item in enumerate(self.form_items):
            if j >= len(data):
                return
            self.form_items[item].set(data[j])

    def set(self, item, value):
        self.form_items[item].set(value)
