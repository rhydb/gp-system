from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from DatabaseHandler import DB
from Table import Table
from Form import Form
from ScrolledFrame import ScrolledFrame

class Therapist(Tk):
    def __init__(self, username, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.username = "gary"
        self.db = DB() # connect to the database

        patient_id_frame = Frame(self)
        Label(patient_id_frame, text="Patient ID:").grid(row=0, column=0)
        self.patient_id_entry = Entry(patient_id_frame)
        self.patient_id_entry.grid(row=0, column=1)
        Button(patient_id_frame, text="Get Details", command=self.get_details).grid(row=0, column=2)
        patient_id_frame.pack()
        
        container = Frame(self)

        left = Frame(container)
        right = Frame(container)

        # left side
        self.records = Text(left)
        self.records.grid()
        Button(left, text="Save Records", command=self.save_records).grid()

        # right side

        # treatment entry
        treatment_frame = Frame(right)
        Label(treatment_frame, text="Treatment name").grid(row=0, column=0)
        Label(treatment_frame, text="Treatment cost").grid(row=0, column=1)
        self.treatment_name = Entry(treatment_frame)
        self.treatment_name.grid(row=1, column=0)
        self.treatment_cost = Entry(treatment_frame)
        self.treatment_cost.grid(row=1, column=1)
        treatment_frame.pack()

        Button(right, text="Save treatment", command=self.save_treatment).pack()
        scrolled_frame = ScrolledFrame(right)
        self.treatments_table = Table(scrolled_frame.interior, rows=3,
              columns=len(self.db.column_indexes["therapists"])-1,
              widths=20)
        self.treatments_table.pack()
        scrolled_frame.pack()

        left.grid(row=0, column=0)
        right.grid(row=0, column=1)
        container.pack()

    def get_details(self):
        try:
            patient_id = int(self.patient_id_entry.get()) # try and cast it to an integer
        except Exception:
            # the patient id is not a number
            messagebox.showerror(title="Invalid Patient ID", message="The patient ID must be a number")
        else:
            # nothing went wrong
            # search for the patient in the patients table
            result = self.db.b_search(patient_id, self.db.column_indexes["patients"]["patient_id"], table="patients")
            if not result:
                # the patient does not exist
                messagebox.showinfo(title="Invalid Patient ID", message="There is no patient with that ID")
                return
            # the patient is valid
            result = self.db.search("therapists", [[self.db.column_indexes["therapists"]["patient_id"], patient_id], [self.db.column_indexes["therapists"]["username"], self.username]], strict=True)
            if not result:
                # the patient has no records with this therapist
                self.db.insert({
                    "patient_id": patient_id,
                    "username": self.username,
                    "record": ""
                }, "therapists")
                messagebox.showinfo(title="Record created", message="That patient did not have a record with you - created one")
            else:
                self.records.delete("1.0", END) # clear the text box
                self.records.insert(END, result[0][self.db.column_indexes["therapists"]["records"]])
                treatments = self.db.search("treatments", [[self.db.column_indexes["treatments"]["patient_id"], patient_id]], strict=True)
                self.treatments_table.set_row_count(len(treatments))
                for j, row in enumerate(treatments):
                    self.treatments_table.set_row(j, row[1:])
        
    def save_records(self):
        try:
            patient_id = int(self.patient_id_entry.get()) # try and cast it to an integer
        except Exception:
            # the patient id is not a number
            messagebox.showerror(title="Invalid Patient ID", message="The patient ID must be a number")
        else:
            # nothing went wrong
            # search for the patient in the patients table
            result = self.db.b_search(patient_id, self.db.column_indexes["patients"]["patient_id"], table="patients")
            if not result:
                # the patient does not exist
                messagebox.showinfo(title="Invalid Patient ID", message="There is no patient with that ID")
                return
            # the patient is valid
            result = self.db.search("therapists", [[self.db.column_indexes["therapists"]["patient_id"], patient_id], [self.db.column_indexes["therapists"]["username"], self.username]], strict=True)
            if not result:
                # the patient has no records with this therapist
                self.db.insert({
                    "patient_id": patient_id,
                    "username": self.username,
                    "record": ""
                }, "therapists")
                messagebox.showinfo(title="Record created", message="That patient did not have a record with you - created one")
            else:
                # update the patient's record
                self.db.update_unsorted("therapists",
                                        [
                                            [self.db.column_indexes["therapists"]["patient_id"], patient_id],
                                            [self.db.column_indexes["therapists"]["username"], self.username]
                                         ],
                                        [
                                            [self.db.column_indexes["therapists"]["records"], self.records.get("1.0", END)]
                                        ],
                                        only_first=True)
                messagebox.showinfo(title="Success", message="Saved")
        
    def save_treatment(self):
        try:
            patient_id = int(self.patient_id_entry.get()) # try and cast it to an integer
        except Exception:
            # the patient id is not a number
            messagebox.showerror(title="Invalid Patient ID", message="The patient ID must be a number")
        else:
            # nothing went wrong
            # search for the patient in the patients table
            result = self.db.b_search(patient_id, self.db.column_indexes["patients"]["patient_id"], table="patients")
            if not result:
                # the patient does not exist
                messagebox.showinfo(title="Invalid Patient ID", message="There is no patient with that ID")
                return
            # the patient is valid
            result = self.db.search("therapists", [[self.db.column_indexes["therapists"]["patient_id"], patient_id], [self.db.column_indexes["therapists"]["username"], self.username]], strict=True)
            if not result:
                # the patient has no records with this therapist
                self.db.insert({
                    "patient_id": patient_id,
                    "username": self.username,
                    "record": ""
                }, "therapists")
                messagebox.showinfo(title="Record created", message="That patient did not have a record with you - created one")
            else:
                # update the patient's treatments
                if not self.treatment_name.get():
                    messagebox.showerror(title="Invalid treatment name", message="Please enter a treatment name")
                    return
                try:
                    cost = float(self.treatment_cost.get())
                except Exception:
                    messagebox.showerror(title="Invalid cost", message="Cost must be a number")
                else:
                    if cost < 0:
                        messagebox.showerror(title="Invalid cost", message="Cost must be > 0")
                        return
                    self.db.insert({
                        "patient_id": patient_id,
                        "treatment": self.treatment_name.get(),
                        "cost": cost
                    }, "treatments")
                    messagebox.showinfo(title="Success", message="Saved")
