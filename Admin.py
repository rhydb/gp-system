from tkinter import *
from DatabaseHandler import DB
from tkinter import messagebox
import NewUserForm

class Admin(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.db = DB() # connect to the database
        self.form_frame = Frame(self)
        self.form_items = []
        self.form_frame.pack()
        self.form = NewUserForm.new_user_form
        self.create_new_patient_form()
    def create_new_patient_form(self):
        for j, item in enumerate(self.form):
            # add a label to the grid and add (*) if it is a required field
            Label(self.form_frame, text=(item.get("name") + (" (*)" if item.get("required") else ""))).grid(row=j, column=0)

            # create the correct widget based on the type specified
            if item.get("type") == "entry":
                self.form_items.append(StringVar())# add it to the list - to get the values back later
                Entry(self.form_frame, textvariable=self.form_items[-1]).grid(row=j, column=1)

            elif item.get("type") == "dropdown":
                self.form_items.append(StringVar()) # add it to the list - to get the values back later
                # create a drop down with the items specified
                OptionMenu(self.form_frame, self.form_items[-1], *item.get("menu_items")).grid(row=j, column=1, sticky="E")

        Button(self.form_frame, text="Get Patient Details", command=self.get_details).grid(row=j+1, column=0, sticky="W")
        Button(self.form_frame, text="Save/Register", command=self.save).grid(row=j+1, column=1, sticky="E")

    def save(self):
        # TODO:
        # if the patient id is not present
        #   - attempt to create a new patient
        # else:
        #   - attempt to update the patient details using the patient id 
        # messagebox with teh result
        data = {}
        for j, item in enumerate(self.form):
            if self.form_items[j].get() == "":
                if item.get("required") is True and self.form_items[j].get() == "" and self.form_items[0].get() == "":
                    # it is required but blank AND the patient ID is empty,
                    # meaning a new user is being created therefore everything must be filled in
                    messagebox.showerror(title="Error", message="Please fill in all nescessary entries (marked with *)")
                    return # cannot proceed
                # format the name of the form item so that it can be used as a datbase column then
                # set the key value pair to the name with the contents of the corresponding field in the form
            else:
                data[item["name"].lower().replace(" ", "_").replace("-", "")] = self.form_items[j].get() 

        if self.form_items[0].get() != "":
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
            patient_id = int(self.form_items[0].get())
        except Exception:
            messagebox.showerror(title="Error", message="Patient ID must be a number")
        else:
            result = self.db.search("patients", [[0, patient_id]], strict=True)
            if len(result) == 0:
                messagebox.showinfo(title="Info", message="Could not find a patient with that ID")
                return
            for j, info in enumerate(result[0]):
                self.form_items[j].set(info)
