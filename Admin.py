from tkinter import *
from DatabaseHandler import DB
from tkinter import messagebox
import NewUserForm
from Table import Table

class Admin(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.db = DB() # connect to the database
        self.patient_edit_frame = Frame(self)
        self.patient_edit_items = []
        self.patient_edit_frame.pack()
        self.patient_edit = NewUserForm.new_user_form
        self.create_new_patient_form()

        self.patient_search_frame = Frame(self)
        self.patient_search_frame.pack()
        self.create_search_form()

    def create_search_form(self):
        Label(self.patient_search_frame, text="Search for a patient").grid()
        Table(self.patient_search_frame, rows=len(self.db.patients_cols), columns=5).grid()
        
    def create_new_patient_form(self):
        Label(self.patient_edit_frame, text="Leave the patient ID blank to create a new patient.").grid()
        for j, item in enumerate(self.patient_edit):
            # add a label to the grid and add (*) if it is a required field
            Label(self.patient_edit_frame, text=(item.get("name") + (" (*)" if item.get("required") else ""))).grid(row=j+1, column=0)

            # create the correct widget based on the type specified
            if item.get("type") == "entry":
                self.patient_edit_items.append(StringVar())# add it to the list - to get the values back later
                Entry(self.patient_edit_frame, textvariable=self.patient_edit_items[-1]).grid(row=j+1, column=1)

            elif item.get("type") == "dropdown":
                self.patient_edit_items.append(StringVar()) # add it to the list - to get the values back later
                # create a drop down with the items specified
                OptionMenu(self.patient_edit_frame, self.patient_edit_items[-1], *item.get("menu_items")).grid(row=j+1, column=1, sticky="E")

        Button(self.patient_edit_frame, text="Get Patient Details", command=self.get_details).grid(row=j+2, column=0, sticky="W")
        Button(self.patient_edit_frame, text="Save/Register", command=self.save).grid(row=j+2, column=1, sticky="E")

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

    def get_details(self):
        try:
            patient_id = int(self.patient_edit_items[0].get())
        except Exception:
            messagebox.showerror(title="Error", message="Patient ID must be a number")
        else:
            result = self.db.search("patients", [[0, patient_id]], strict=True)
            if len(result) == 0:
                messagebox.showinfo(title="Info", message="Could not find a patient with that ID")
                return
            for j, info in enumerate(result[0]):
                self.patient_edit_items[j].set(info)
