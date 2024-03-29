from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from DatabaseHandler import DB
from Table import Table
from Form import Form
from ScrolledFrame import ScrolledFrame

class DrNurse(Tk): # the window to contain the dr nurse window that inherits from the Tk obejct
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs) # call the tk object that htis inherits from
        self.db = DB() # connect to the database
        self.patient_id = int # will be used to store the patient id that the information will be stored to
        Label(self, text="Patient ID:").pack()
        self.patient_id_entry = Entry(self)
        self.patient_id_entry.pack()
        # buttons that call the methods to search and save
        Button(self, text="Get details", command=self.get_info).pack()
        Button(self, text="Save All", command=self.save_all).pack()
        patient_details_frame = Frame(self)
        
        # create a textbox  for each piece of information about the patient
        history_frame = Frame(patient_details_frame)
        Label(history_frame, text="Medical History").grid()
        self.history = Text(history_frame)
        self.history.grid()
        history_frame.grid(row=0, column=0)

        details_frame = Frame(patient_details_frame)
        Label(details_frame, text="Consultations and Medicine").grid()
        self.details = Text(details_frame)
        self.details.grid()
        details_frame.grid(row=0, column=1)

        referals_frame = Frame(patient_details_frame)
        Label(referals_frame, text="Referals").grid()
        self.referals = Text(referals_frame)
        self.referals.grid()
        referals_frame.grid(row=1, column=0)

        tests_frame = Frame(patient_details_frame)
        Label(tests_frame, text="Tests").grid()
        self.tests = Text(tests_frame)
        self.tests.grid()
        tests_frame.grid(row=1, column=1)

        patient_details_frame.pack() # add everything to the window


    def clear_all(self): # used when searching for patients to clear the previous results
        self.history.delete("1.0", END)
        self.details.delete("1.0", END)
        self.referals.delete("1.0", END)
        self.tests.delete("1.0", END)

    def get_info(self): # to get the details of a patient
        # check if the patient id is a number
        try:
            patient_id = int(self.patient_id_entry.get())
        except Exception:
            messagebox.showerror(title="Error", message="Patient ID must be an integer")
        else:
            # nothing went wrong
            results = self.db.b_search(patient_id, 0, table="patients") # search for the patient using binary search to get the patients details
            if not results:
                messagebox.showerror(title="Error", message="Could not find a patient with that ID")
                return
            self.patient_id = patient_id
            self.clear_all()
            # use the dicitonairy in the database handler to get the column index of each details about the patient
            # then get the piece of information from the results and insert it into the text box
            # if there are no details insert an empty string
            self.history.insert(INSERT, results[self.db.column_indexes["patients"]["history"]] if results[self.db.column_indexes["patients"]["history"]] else '')
            self.details.insert(INSERT, results[self.db.column_indexes["patients"]["details"]] if results[self.db.column_indexes["patients"]["details"]] else '')
            self.referals.insert(INSERT, results[self.db.column_indexes["patients"]["referals"]] if results[self.db.column_indexes["patients"]["referals"]] else '')
            self.tests.insert(INSERT, results[self.db.column_indexes["patients"]["tests"]] if results[self.db.column_indexes["patients"]["tests"]] else '')
        
    def save_all(self):
        # create an array with the column each piece of information relates to in the database and the piece of data
        data = [
            [self.db.column_indexes["patients"]["history"], self.history.get("1.0", END).replace("\\", "backslash!")],
            [self.db.column_indexes["patients"]["details"], self.details.get("1.0", END).replace("\\", "backslash!")],
            [self.db.column_indexes["patients"]["referals"], self.referals.get("1.0", END).replace("\\", "backslash!")],
            [self.db.column_indexes["patients"]["tests"], self.tests.get("1.0", END).replace("\\", "backslash!")]
        ]
        self.db.update(self.patient_id, "patients", data) # update the patients details in the database
        messagebox.showinfo(title="Success", message="Saved")
        
