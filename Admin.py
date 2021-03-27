from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from DatabaseHandler import DB
import NewUserForm
from Table import Table
from ScrolledFrame import ScrolledFrame

class Admin(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.db = DB() # connect to the database

        # create the tabs
        self.tab_control = ttk.Notebook(self) # the tab manager that holds each 'button' to switch tab
        # these act as frames to place items into
        self.patient_tab = ttk.Frame(self.tab_control)
        self.search_tab = ttk.Frame(self.tab_control)
        self.appointment_tab = ttk.Frame(self.tab_control)
        
        self.patient_edit_items = [] # each form entry will store a stringvar() in here which can be used to fetch the input
        self.patient_tab.pack()
        self.patient_edit = NewUserForm.new_user_form # TODO: add the form back in
        self.create_new_patient_form()

        self.patient_search_frame = Frame(self)
        self.search_items = [] # will store all the widgets in the search that allows a .get() to fetch the data inside
        self.strict_search = False
        self.patient_search_frame.pack()
        self.search_table = Table
        self.create_search_form()

        self.tab_control.add(self.patient_tab, text="Add/Edit Patient")
        self.tab_control.add(self.search_tab, text="Patient Search")
        self.tab_control.pack(expand=True, fill=BOTH)
    
    def search(self):
        # make a list of all the search entries that arent empty and
        # record which column they refer to - needed to search the databse
        queries = [[j, item.get()] for j, item in enumerate(self.search_items) if item.get()]
        results = self.db.search("patients", queries, strict=self.strict_search)
        self.search_table.set_row_count(len(results))
        for j, result in enumerate(results):
            self.search_table.set_row(j, result)


        
    def create_search_form(self):
        Label(self.search_tab, text="Search for a patient").pack()
        entry_frame = Frame(self.search_tab) # frame to hold the entries and search button in one line

        for j, item in enumerate(self.patient_edit):
            # create the correct widget based on the type specified
            if item.get("type") == "entry":
                # TODO: find a way to append a string var at the end of the if checks
                self.search_items.append(StringVar())# add it to the list - to get the values back later
                Entry(entry_frame, textvar=self.search_items[-1]).grid(row=0, column=j)
            elif item.get("type") == "dropdown":
                self.search_items.append(StringVar()) # add it to the list - to get the values back later
                OptionMenu(entry_frame, self.search_items[-1], *item.get("menu_items")).grid(row=0, column=j)

        entry_frame.pack()
        # add a results label, button to search and a checkbox to toggle strict searching below the center of the table
        Button(entry_frame, text="Search", command=self.search).grid(row=1, column=j//2)
        Checkbutton(entry_frame, text="Strict Search", variable=self.strict_search, onvalue=True, offvalue=False, command=self.toggle_strict_search).grid(row=1, column=1+j//2)
        scrolled_frame = ScrolledFrame(self.search_tab)
        # create a table with enough columns and headers for each of the column names
        # it gets the column count from the database handler and the names from the patient edit form
        # TODO: get the column headers from the data base handler as well
        self.search_table = Table(scrolled_frame.interior, columns=len(self.db.patients_cols), rows=5, show_headers=True, headers=[item["name"] for item in self.patient_edit])
        self.search_table.pack()
        scrolled_frame.pack()
        
    def create_new_patient_form(self):
        form_frame = Frame(self.patient_tab) # inner frame to contain all of the widgets on the new patient tab
        Label(form_frame, text="Leave the patient ID blank to create a new patient.").grid()
        for j, item in enumerate(self.patient_edit):
            # add a label to the grid and add (*) if it is a required field
            Label(form_frame, text=(item.get("name") + (" (*)" if item.get("required") else ""))).grid(row=j+1, column=0)

            # create the correct widget based on the type specified
            if item.get("type") == "entry":
                # TODO: append a string var at end of if statment instead of both
                self.patient_edit_items.append(StringVar())# add it to the list - to get the values back later
                Entry(form_frame, textvariable=self.patient_edit_items[-1]).grid(row=j+1, column=1)

            elif item.get("type") == "dropdown":
                self.patient_edit_items.append(StringVar()) # add it to the list - to get the values back later
                # create a drop down with the items specified
                OptionMenu(form_frame, self.patient_edit_items[-1], *item.get("menu_items")).grid(row=j+1, column=1, sticky="E")

        Button(form_frame, text="Get Patient Details", command=self.get_details).grid(row=j+2, column=0, sticky="W")
        Button(form_frame, text="Save/Register", command=self.save).grid(row=j+2, column=1, sticky="E")
        form_frame.pack(expand=True)

    def save(self):
        data = {}
        for j, item in enumerate(self.patient_edit):
            if self.patient_edit_items[j].get() == "":
                if item.get("required") is True and self.patient_edit_items[j].get() == "" and self.patient_edit_items[0].get() == "":
                    # it is required but blank AND the patient ID is empty,
                    # meaning a new user is being created therefore everything must be filled in
                    messagebox.showerror(title="Error", message="Please fill in all nescessary entries (marked with *)")
                    return # cannot proceed
                # format the name of the form item so that it can be used as a datbase column then
                # set the key value pair to the name with the contents of the corresponding field in the form
            else:
                data[item["name"].lower().replace(" ", "_").replace("-", "")] = self.patient_edit_items[j].get() 

        if self.patient_edit_items[0].get() != "":
            try:
                data["patient_id"] = int(data.get("patient_id"))
            except Exception:
                messagebox.showerror(title="Error", message="Invalid Patient ID")
            else:
                messagebox.showinfo(title="Info", message=self.db.update_patient(data))
        else:
            # patient id was omitted -> make a new patient
            messagebox.showinfo(title="Info", message=self.db.create_patient(data))

    # search for a patient using the id, and set all the entries to the patient's details to allow editing
    # uses a recursive binary search as the patient id is a primary key and is sorted
    def get_details(self):
        # try and cast the input to an integer as the patient id is an integer
        try:
            patient_id = int(self.patient_edit_items[0].get())
        except Exception:
            messagebox.showerror(title="Error", message="Patient ID must be a number")
        else:
            # casting to an integer was a success, proceed with the search
            result = self.db.b_search_patient(patient_id)
            if not result:
                messagebox.showinfo(title="Info", message="Could not find a patient with that ID")
                return
            for j, info in enumerate(result):
                self.patient_edit_items[j].set(info)

    def toggle_strict_search(self):
        # used when the checkbox is clicked to toggle strict searchign
        self.strict_search = not self.strict_search
