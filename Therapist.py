from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from DatabaseHandler import DB # this will be used to connect to the database file
# these modules will create custom forms and tables
from Table import Table
from Form import Form
from ScrolledFrame import ScrolledFrame # to add scrollbars to things

class Therapist(Tk): # create a class for the window that inherits from the Tk object
    def __init__(self, username, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.username = username # the username that was used to login is used to collect only the nescessary information about a patient
        self.db = DB() # create a database handler to connect to the database handler

        patient_id_frame = Frame(self) # a fram to organise the label, entry and button for entering a patient Id in a row
        Label(patient_id_frame, text="Patient ID:").grid(row=0, column=0)
        self.patient_id_entry = Entry(patient_id_frame)
        self.patient_id_entry.grid(row=0, column=1)
        Button(patient_id_frame, text="Get Details", command=self.get_details).grid(row=0, column=2)# when clicked -> get all the details of the patient related to the logged in therapist and display them in the table and text box
        patient_id_frame.pack() # add it to the window
        
        container = Frame(self) # container is a frame that will be below the patient Id entry that contains the left and right side
        left = Frame(container) # left side of the container
        right = Frame(container) # right side of the container

        # left side
        Label(left, text="Medical Records").grid()
        self.records = Text(left)
        self.records.grid()
        Button(left, text="Save Records", command=self.save_records).grid() # when clicked ->  save the updated records to the database

        # right side

        # creeate a small form to input the treatment and the cost
        treatment_frame = Frame(right) # will contain both labels and entry boxes
        Label(treatment_frame, text="Treatment name").grid(row=0, column=0)
        Label(treatment_frame, text="Treatment cost").grid(row=0, column=1)
        self.treatment_name = Entry(treatment_frame)
        self.treatment_name.grid(row=1, column=0)
        self.treatment_cost = Entry(treatment_frame)
        self.treatment_cost.grid(row=1, column=1)
        treatment_frame.pack()

        Button(right, text="Save treatment", command=self.save_treatment).pack() # when clicked -> add the treatment to the database
        scrolled_frame = ScrolledFrame(right) # a scrollbar for the table
        self.treatments_table = Table(scrolled_frame.interior, rows=3, # create a table to display all treatments and their cost for the patient
              columns=len(self.db.column_indexes["therapists"])-1, # fetch the amount of columns from the column index dictionairy in the database handler
              widths=20) # set the width of each entry box
        # add everything to the window
        self.treatments_table.pack()
        scrolled_frame.pack()

        left.grid(row=0, column=0)
        right.grid(row=0, column=1)
        container.pack()

    # method called by the "Get Details" button to fetch all the details about the patient using the patient ID and update the textbox and table
    def get_details(self):
        try:
            patient_id = int(self.patient_id_entry.get()) # get the entered patient ID and try to cast it to an integer
        except Exception: # if the casting to int failed the error will be caught here
            # the patient id is not a number so display a messagebox
            messagebox.showerror(title="Invalid Patient ID", message="The patient ID must be a number")
        else:
            # nothing went wrong so the patient Id in an integer
            # search for the patient in the patients table
            # since the patients table is sorted by the patient id a binary search can be used to see if the patient exists in the table
            result = self.db.b_search(patient_id, self.db.column_indexes["patients"]["patient_id"], table="patients") 
            if not result: # b_search returns None if not found
                # the patient does not exist, display a messagebox with the error
                messagebox.showinfo(title="Invalid Patient ID", message="There is no patient with that ID")
                return
            # the patient is valid, get the row in the therapists table with all the information
            result = self.db.search("therapists", [[self.db.column_indexes["therapists"]["patient_id"], patient_id], [self.db.column_indexes["therapists"]["username"], self.username]], strict=True)
            if not result: # search will return nothing if the row does not exist
                # the patient has no records with this therapist so create a blank row in the database
                self.db.insert({
                    "patient_id": patient_id,
                    "username": self.username,
                    "record": ""
                }, "therapists")
                messagebox.showinfo(title="Record created", message="That patient did not have a record with you - created one") # inform the user what happened
            else: # there is already a record with this patient and therapist
                # clear the textbox and insert the searched for patient's record
                self.records.delete("1.0", END)
                self.records.insert(END, result[0][self.db.column_indexes["therapists"]["records"]])
                # get all the treatments for the patient and therapist and update the table to display them
                treatments = self.db.search("treatments", [[self.db.column_indexes["treatments"]["patient_id"], patient_id]], strict=True)
                # set the row count of the table to the number of treatments they had
                self.treatments_table.set_row(0, ["", ""]) # clear the first row incase there are no results
                self.treatments_table.set_row_count(max(1, len(treatments))) # max(1, ) is to avoid the table dissappearing because of no results
                for j, row in enumerate(treatments): # go through each result and the row in the table to hold that information
                    self.treatments_table.set_row(j, row[1:])
    
    # a method called by the "Save Records" Button below the textbox to update the database 
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
                # the patient does not exist, display a messagebox with the error
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
            # the patient id is not a number exists
            messagebox.showerror(title="Invalid Patient ID", message="The patient ID must be a number")
        else:
            # nothing went wrong
            # search for the patient in the patients table
            result = self.db.b_search(patient_id, self.db.column_indexes["patients"]["patient_id"], table="patients")
            if not result:
                # the patient does not exist in the patients tables, display a messagebox with the error
                messagebox.showinfo(title="Invalid Patient ID", message="There is no patient with that ID")
                return
            # the patient id is valid and the patient
            result = self.db.search("therapists", [[self.db.column_indexes["therapists"]["patient_id"], patient_id], [self.db.column_indexes["therapists"]["username"], self.username]], strict=True)
            if not result:
                # the patient has no records with this therapist so create a blank record
                self.db.insert({
                    "patient_id": patient_id,
                    "username": self.username,
                    "record": ""
                }, "therapists")
                messagebox.showinfo(title="Record created", message="That patient did not have a record with you - created one") # let the user know what happened
            else:
                # update the patient's treatments
                if not self.treatment_name.get(): # the treatment name was blank se
                    messagebox.showerror(title="Invalid treatment name", message="Please enter a treatment name") # display the error
                    return
                try: # get the tratment cost and try to cast to a float
                    cost = float(self.treatment_cost.get())
                except Exception: # catch any errors that happen when casting to a float
                    messagebox.showerror(title="Invalid cost", message="Cost must be a number") # let the user know the error
                else:
                    if cost < 0: # the cost cannot be negative
                        messagebox.showerror(title="Invalid cost", message="Cost must be greater than 0") # let the user know
                        return
                    # the treatment name is not blank and the cost is valid, insert the tratment into the database
                    self.db.insert({
                        "patient_id": patient_id,
                        "treatment": self.treatment_name.get(),
                        "cost": cost
                    }, "treatments")
                    # update the table with the new row
                    self.treatments_table.add_row()
                    self.treatments_table.set_row(self.treatments_table.rows-1, [self.treatment_name.get(), cost]) 
                    messagebox.showinfo(title="Success", message="Saved") # display a messagebox showing that it has saved
