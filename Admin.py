from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from DatabaseHandler import DB
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
        self.appointment_tab = ttk.Frame(self.tab_control)


        # setup for the patient tab
        patient_table_scroll = ScrolledFrame(self.patient_tab)
        self.patient_table = Table(patient_table_scroll.interior, columns=len(self.db.patients_cols), rows=5, show_headers=True, headers=[item["display_name"] for item in self.db.patient_form], widths=[item["width"] for item in self.db.patient_form])
        self.patient_table.pack()
        patient_table_scroll.grid(row=0, column=0)

        self.patient_form = Form(self.patient_tab, data=self.db.patient_form)
        self.patient_form.grid(row=0, column=1)
        Button(self.patient_form, text="Get Patient Details", command=self.get_patient_details).grid()
        Button(self.patient_form, text="Search", command=self.search_patient).grid(row=len(self.patient_form.form_items), column=1)
        self.strict_search = False
        Checkbutton(self.patient_form, text="Strict", variable=self.strict_search, onvalue=True, offvalue=False, command=self.toggle_strict_search).grid(row=len(self.patient_form.form_items)+1, column=1)
        Button(self.patient_form, text="Save/Register", command=self.save_patient).grid(row=len(self.patient_form.form_items), column=2)
        self.patient_tab.pack()

        # setup for the appointments tab
        appointments_scrolled_frame = ScrolledFrame(self.appointment_tab)
        self.appointments_table = Table(appointments_scrolled_frame, rows=3, columns=len(self.db.appointment_form), show_headers=True, headers=[item["display_name"] for item in self.db.appointment_form], widths=[item["width"] for item in self.db.appointment_form])
        self.appointments_table.pack()
        appointments_scrolled_frame.grid(row=0, column=0)
        self.appointments_form = Form(self.appointment_tab, data=self.db.appointment_form)
        Button(self.appointments_form, text="Search with Patient ID", command=self.search_appointment).grid(row=len(self.db.appointment_form), column=0)
        Button(self.appointments_form, text="Canel Appointment", command=self.cancel_appointment).grid(row=len(self.db.appointment_form), column=1)
        Button(self.appointments_form, text="Book", command=self.book_appointment).grid(row=len(self.db.appointment_form), column=2)
        self.appointments_form.grid(row=0, column=1)

        

        self.tab_control.add(self.patient_tab, text="Add/Edit Patient")
        self.tab_control.add(self.appointment_tab, text="Appointments")
        self.tab_control.pack(expand=True, fill=BOTH)

    def book_appointment(self):
        self.appointments_form.set("appointment_id", "")
        if not self.appointments_form.completed_required():
            messagebox.showerror(title="Error", message="Please fill in all nescessary entries (marked with *)")
            return
        if self.appointments_form.get("patient_id"):
            try:
                patient_id = int(self.appointments_form.get("patient_id"))
            except Exception:
                messagebox.showerror(title="Invalid patient ID", message="The patient ID must be an integer")
                return
            else:
                if not self.db.b_search(patient_id, 0, table="patients"):
                    messagebox.showerror(title="Invalid patient ID", message="There isn't a patient with that ID")
                    return
        data = {}
        for key, value in self.appointments_form.form_items.items():
            if value.get():
                data[key] = value.get()
        messagebox.showinfo(title="Success", message="New appointment with ID:" + str(self.db.insert(data, "appointments")))
        
    def search_appointment(self):
        try:
            patient_id = int(self.appointments_form.get("patient_id"))
        except Exception:
            messagebox.showerror(title="Error", message="Invalid patient ID")
        else:
            results = self.db.search("appointments", [[1, patient_id]], strict=True)
            if results:
                self.appointments_table.set_row_count(len(results))
                for j, result in enumerate(results):
                    self.appointments_table.set_row(j, result)
            else:
                messagebox.showinfo(title="No results", message="There were no results for your query")

    def cancel_appointment(self):
        try:
            appointment_id = int(self.appointments_form.get("appointment_id"))
        except Exception:
            messagebox.showerror(title="Error", message="Invalid appointment ID")
        else:
            row_number = self.db.b_search(appointment_id, 0, table="appointments", get_row_number=True)
            if not row_number:
                messagebox.showerror(title="Error", message="Could not find an appointment with that ID")
                return
            self.db.delete_row("appointments", row_number)
            messagebox.showinfo(title="Cancelled", message="Appointment cancelled")
    def search_patient(self):
        # make a list of all the search entries that arent empty and
        # record which column they refer to - needed to search the databse
        queries = [[j, item.get()] for j, item in enumerate(self.patient_form.form_items.values()) if item.get()]
        results = self.db.search("patients", queries, strict=self.strict_search)
        if results:
            self.patient_table.set_row_count(len(results))
            for j, result in enumerate(results):
                self.patient_table.set_row(j, result)
        else:
            messagebox.showinfo(title="No results", message="Could not find any results for that query")

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
            messagebox.showinfo(title="Info", message="New Patient with ID: " + str(self.db.insert(data, "patients")))

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
            result = self.db.b_search(patient_id, 0, "patients")
            if not result:
                messagebox.showinfo(title="Info", message="Could not find a patient with that ID")
                return
            self.patient_form.set_all(result)

    def toggle_strict_search(self):
        # used when the checkbox is clicked to toggle strict searching
        self.strict_search = not self.strict_search
