from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from DatabaseHandler import DB
import NewUserForm
from Table import Table
from Form import Form
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


        self.patient_edit = NewUserForm.new_user_form # TODO: add the form back in
        
        # setup for the patient details menu
        Label(self.patient_tab, text="Leave the patient ID blank to create a new patient.").pack()
        self.patient_form = Form(self.patient_tab, data=self.patient_edit, display="block")
        self.patient_form.pack(expand=True)
        Button(self.patient_form, text="Get Patient Details", command=self.get_patient_details).grid(sticky="W")
        Button(self.patient_form, text="Save/Register", command=self.save_patient).grid(row=len(self.patient_form.form_items), column=1, sticky="E")
        self.patient_tab.pack()

        # setup for the search tab
        self.patient_search_frame = Frame(self)
        self.search_items = [] # will store all the widgets in the search that allows a .get() to fetch the data inside
        self.strict_search = False
        self.patient_search_frame.pack()
        self.search_table = Table
        self.create_search_form()

        self.create_appointments_form()

        self.tab_control.add(self.patient_tab, text="Add/Edit Patient")
        self.tab_control.add(self.search_tab, text="Patient Search")
        self.tab_control.add(self.appointment_tab, text="Appointments")
        self.tab_control.pack(expand=True, fill=BOTH)

    def create_appointments_form(self):
        table = Table(self.appointment_tab, rows=5, columns=len(self.db.appointment_cols), show_headers=True, headers=self.db.appointment_cols)
        table.pack()
    
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
        
    def save_patient(self):
        if not self.patient_form.completed_required():
            messagebox.showerror(title="Error", message="Please fill in all nescessary entries (marked with *)")
            return
        data = {}
        for key, value in self.patient_form.form_items.items():
            if value.get():
                data[key] = value.get()

        if data.get("patient_id"):
            try:
                data["patient_id"] = int(data.get("patient_id"))
            except Exception:
                messagebox.showerror(title="Error", message="Invalid Patient ID")
            else:
                # id was provided and the id was an integer
                messagebox.showinfo(title="Info", message=self.db.update_patient(data))
        else:
            # patient id was omitted -> make a new patient
            messagebox.showinfo(title="Info", message=self.db.create_patient(data))

    # search for a patient using the id, and set all the entries to the patient's details to allow editing
    # uses a recursive binary search as the patient id is a primary key and is sorted
    def get_patient_details(self):
        # try and cast the input to an integer as the patient id is an integer
        try:
            patient_id = int(self.patient_form.get("patient_id"))
        except Exception:
            messagebox.showerror(title="Error", message="Patient ID must be a number")
        else:
            # casting to an integer was a success, proceed with the search
            result = self.db.b_search_patient(patient_id)
            if not result:
                messagebox.showinfo(title="Info", message="Could not find a patient with that ID")
                return
            self.patient_form.set(result)

    def toggle_strict_search(self):
        # used when the checkbox is clicked to toggle strict searching
        self.strict_search = not self.strict_search
