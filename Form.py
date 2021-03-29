from tkinter import *

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
            Label(self, text=(item.get("display_name"))).grid(row=(j if display == "block" else 0), column=(0 if display == "block" else j))
            if item.get("type") == "entry":
                Entry(self, textvar=self.form_items[item.get("name")]).grid(row=(j if display == "block" else 1), column=(1 if display == "block" else j))
            elif item.get("type") == "dropdown":
                OptionMenu(self, self.form_items[item.get("name")], *item.get("menu_items")).grid(row=(j if display == "block" else 1), column=(1 if display == "block" else j))

    def completed_required(self):
        for item in self.data:
            if item.get("required") and not self.form_items[item["name"]].get():
                return False
        return True
    def get(self, name):
        return self.form_items.get(name).get() # return the given item's content
    def get_all(self):
        return [item.get() for item in self.form_items.values()] # make a list out of all the items' stringvar's
    def set(self, data):
        for j, item in enumerate(self.form_items):
            if j >= len(data):
                return
            self.form_items[item].set(data[j])
