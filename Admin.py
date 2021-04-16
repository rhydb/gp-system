from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from DatabaseHandler import DB # database handler to interact with the datbase
from Table import Table # to create custom tables
from Form import Form # to create a form of widgets from a dictionary
from ScrolledFrame import ScrolledFrame # to add scrollbars to things
from DateValidator import is_valid_date # used to validate the dates that are entered

class Admin(Tk): # admin window inherits from the Tk() obejct
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs) # call the Tk() object that this inherits from
        self.db = DB() # database handler to interact with the database

        # create the tabs
        self.tab_control = ttk.Notebook(self) # the tab manager that holds each 'button' to switch tab
        # these act as frames to place items into the seperate tabs
        self.patient_tab = ttk.Frame(self.tab_control)
        self.appointment_tab = ttk.Frame(self.tab_control)
        self.treatment_tab = ttk.Frame(self.tab_control)

        '''
        the patients tab allows for registering new patients, updating the details of existing patients and searching for patients
        using different pieces of information.
        It uses a patient ID to keep each patient unique in the database
        '''
        patient_table_scroll = ScrolledFrame(self.patient_tab) # creates a scrollbar that the table will use
        # create a table inside the scrollbar frame using the columns defined in the patient form dicionary in the database handler
        # the headers will be array created from each item's display name in the patient form
        # each column will have the width specified in the patient form
        # it will display the results from searching for patients
        self.patient_table = Table(patient_table_scroll.interior,
                                    columns=len(self.db.patient_form),
                                    rows=5, show_headers=True,
                                    headers=[
                                        item["display_name"] for item in self.db.patient_form
                                        ],
                                    widths=[item["width"] for item in self.db.patient_form])
        # add everything to the window
        self.patient_table.pack()
        patient_table_scroll.grid(row=0, column=0)

        self.patient_form = Form(self.patient_tab, data=self.db.patient_form) #  create form using the dicitonairy defined in the database handler
        self.patient_form.grid(row=0, column=1)
        Button(self.patient_form, text="Get Patient Details", command=self.get_patient_details).grid() # when clicked -> fetch the details of the patient using the patient ID entered
        Button(self.patient_form, text="Search", command=self.search_patient).grid(row=len(self.patient_form.form_items), column=1) # when clicked -> perform a search on the database using the entered details in the form
        self.strict_search = False # this is toggled in the checkbox through the toggle_strict_search method
        # create a checkbox that will call the toggle_strict_search method to change if it is strict or not
        Checkbutton(self.patient_form, text="Strict",
                    variable=self.strict_search,
                    onvalue=True, 
                    offvalue=False,
                    command=self.toggle_strict_search
                    ).grid(row=len(self.patient_form.form_items)+1, column=1)
        Button(self.patient_form,
                text="Save/Register", 
                command=self.save_patient
                ).grid(row=len(self.patient_form.form_items), column=2) # when clicked -> save or register the patient details depending if the patient id was entered
        Label(self.patient_form, text="Leave the Patient ID blank to create a new patient").grid() # a small label to inform the user how to create a new patient

        self.patient_tab.pack() # add everything to the screen

        '''
        the appointments tab will allow for booking, cancelling and searching for appointments
        it will display a table and form to fill out that can interact with the database
        '''
        appointments_scrolled_frame = ScrolledFrame(self.appointment_tab) # a scrollbar that the apopintments table will use
        self.appointments_table = Table(appointments_scrolled_frame, # create a table with each heading being the item in the appointment form, it will display the results from searching
                                        rows=3,
                                        columns=len(self.db.appointment_form),
                                        show_headers=True,
                                        headers=[
                                            item["display_name"] for item in self.db.appointment_form # fetch all the display names for the headers from the dicitonairy inside the database handler
                                        ],
                                        widths=[
                                            item["width"] for item in self.db.appointment_form # each width is fetched from the dicitionairy inside the database handler
                                        ])
        self.appointments_table.pack()
        appointments_scrolled_frame.grid(row=0, column=0)
        self.appointments_form = Form(self.appointment_tab, # create a form for entering and searching appointments using the dictionairy defined in the database handler
                                        data=self.db.appointment_form)
        # add all the buttons to search, cancel and book appointments
        Button(self.appointments_form,
                text="Search with Patient ID",
                command=self.search_appointment # call the search_appointment method which performs a search on the database
                ).grid(row=len(self.db.appointment_form), column=0)
        Button(self.appointments_form,
                text="Canel Appointment",
                command=self.cancel_appointment # call the cancel_appointment method which deletes the row from the database
                ).grid(row=len(self.db.appointment_form), column=1)
        Button(self.appointments_form,
                text="Book",
                command=self.book_appointment # call the book_appointment method which inserts a new appointment into the database
                ).grid(row=len(self.db.appointment_form), column=2)
        self.appointments_form.grid(row=0, column=1)

        '''
        the treatments tab will allow for fetching all treatments a patient has recieved and the total cost
        it will also allow for creating an invoice in a textbox
        '''
        treatments_scoll = ScrolledFrame(self.treatment_tab) # a scrollbar that the treatments table will use
        self.treatments_table = Table(treatments_scoll.interior, # create a table with each header and column being each item in the treatments form, it will display the results of searching
                                        rows=3,
                                        columns=len(self.db.treatments_form),
                                        show_headers=True,
                                        headers=[
                                            item.get("display_name") for item in self.db.treatments_form
                                        ])
        self.treatments_table.pack()

        self.invoice = Text(self.treatment_tab) # the textbox that will display the invoices created

        Button(self.treatment_tab, # add a button that will calculate the total cost of all the treatments
                text="Get total cost",
                command=lambda: 
                    messagebox.showinfo(
                        title="Total cost",
                        message=self.get_treatments_cost())
                ).grid(row=0,column=0)

        Button(self.treatment_tab, # add a button that will create an invoice using the treatments a patient has been given and their cost 
                text="Create Invoice",
                command=self.create_invoice
                ).grid(row=0,column=1)

        # create a small form that allows for searching the treatments a patient has been given and displaying them in the table
        search_treatment_frame = Frame(self.treatment_tab)
        Label(search_treatment_frame, text="Patient ID:").grid()
        self.treatment_patient_id = Entry(search_treatment_frame)
        self.treatment_patient_id.grid(row=0, column=1)
        Button(search_treatment_frame,
                text="Get treatments",
                command=self.get_treatments # when clicked -> call the get_treatments_method to display all the treatments in the table
                ).grid(row=0, column=2)
        search_treatment_frame.grid()
        treatments_scoll.grid()
        self.invoice.grid(row=2, column=1)
        
        self.treatment_tab.pack()

        # add each tab to the tab control with a title
        self.tab_control.add(self.patient_tab, text="Add/Edit Patient")
        self.tab_control.add(self.appointment_tab, text="Appointments")
        self.tab_control.add(self.treatment_tab, text="Treatments/Invoice")
        self.tab_control.pack(expand=True, fill=BOTH)

    def create_invoice(self): # called by the create invoice button
        self.invoice.delete("0.0", END) # clear the current contents of the textboxs
        # insert some initial information about the invoice (patient id, the total cost)
        self.invoice.insert(END, f"Patient ID: {self.treatments_table.get_cell(0, 0)} Total Cost: {self.get_treatments_cost()}\n")
        self.invoice.insert(END, f'{"Treatment":^20}{"Cost":^10}\n') # the headings for the next pieces of information
        for i in range(self.treatments_table.rows): # for each treatment add its name and cost into the textbox
            row = self.treatments_table.get_row(i) # get the row in the table
            self.invoice.insert(END, f"{row[1]:<20}{row[2]:>10}\n") # insert the data in the row with correct padding to follow the headings created
        
    def get_treatments_cost(self): # a method to calculate the total cost of all the treatments a patient has 
        all_costs = self.treatments_table.get_column("Cost") # get the entire column with all the costs in
        total = sum([float(cost) for cost in all_costs if cost]) # create a list for each item casted as a float in the cost column and calculate the sum
        return total if total else "There are no treatments for that patient" # if the total was 0 there are no treatments
        
    def get_treatments(self): # a method to fetch all the treatments a patient has from the database
        try:
            # get the patient id from the entry box and try to cast it to an integer
            patient_id = int(self.treatment_patient_id.get())
        except Exception: # catch any errors while casting to an integer
            messagebox.showerror(title="Error", message="Invalid patient ID") # something went wrong - let the user know
        else:
            results = self.db.search("treatments", [[0, patient_id]], strict=True) # get all the treatments for that patient from the database
            if not results: # if there were no results the patient doesnt have any treatments
                messagebox.showinfo(title="No results", message="There were no results for your query") # let the user know there are no treatments
                return
            self.treatments_table.set_row_count(len(results)) # set the row count to how many results there are
            for j, result in enumerate(results): # for each treatment add it to the table
                self.treatments_table.set_row(j, result)
        
    def book_appointment(self): # a method to create an appointment for a patient using the information in the form, called by the book appointment button
        self.appointments_form.set("appointment_id", "") # the appointment id must be blank so that it automatically increments
        if not self.appointments_form.completed_required(): # if not all the required entries are filled in let the user know
            messagebox.showerror(title="Error", message="Please fill in all nescessary entries (marked with *)")
            return
        date = self.appointments_form.form_items["date"].get() # get the date entered
        if date and not is_valid_date(date): # if the date is not valid let the user know
            messagebox.showerror(title="Invalid date", message="Invalid date. The date should be in the format dd-mm-yyyy")
            return
        try:
            patient_id = int(self.appointments_form.get("patient_id")) # get the patient id and try to cast it to an integer
        except Exception: # catch any errors while casting to an integer
            messagebox.showerror(title="Invalid patient ID", message="The patient ID must be an integer") # let the user know the patient id was invalid
            return
        else: # the patient id was not entered - register a new user
            if not self.db.b_search(patient_id, 0, table="patients"): # search for the patient id using binary search
                messagebox.showerror(title="Invalid patient ID", message="There isn't a patient with that ID") # could not find the patient let the user know
                return
        data = {} # creaet a dictionairy with a key of the items name and the value it has in the form
        for key, value in self.appointments_form.form_items.items():
            if value.get(): # if the value was entered
                data[key] = value.get() # add it to the dictionairy
        messagebox.showinfo(title="Success", message="New appointment with ID:" + str(self.db.insert(data, "appointments"))) # insert the data into the database and let the user know the id of it
        
    def search_appointment(self): # search for all appointments a patient has
        try:
            patient_id = int(self.appointments_form.get("patient_id")) # try and cast the patient id to an integer
        except Exception: # something went wrong with casting to an integer
            messagebox.showerror(title="Error", message="Invalid patient ID") # let the user know of the error
        else:
            results = self.db.search("appointments", [[1, patient_id]], strict=True) # search for the patient in the database
            if results: # the patient has appointments
                self.appointments_table.set_row_count(len(results)) # add the appointments into the table
                for j, result in enumerate(results):
                    self.appointments_table.set_row(j, result)
            else:
                messagebox.showinfo(title="No results", message="There were no results for your query")

    def cancel_appointment(self): # method to cancel an appointment using the appointment id
        try:
            appointment_id = int(self.appointments_form.get("appointment_id")) # try to cast the appointment id to an integer
        except Exception:
            messagebox.showerror(title="Error", message="Invalid appointment ID") # appointment id is not a number - let the user know
        else:
            row_number = self.db.b_search(appointment_id, 0, table="appointments", get_row_number=True) # get the row the appointment has in the database
            if not row_number: # the appointment does not exist
                messagebox.showerror(title="Error", message="Could not find an appointment with that ID")
                return
            self.db.delete_row("appointments", row_number) # delete the row the appointment is in from the database
            messagebox.showinfo(title="Cancelled", message="Appointment cancelled") # let the user know

    def search_patient(self): # search for a patient using different pieces of information
        # get the date and check if it is valid
        date = self.patient_form.form_items["date_of_birth"].get()
        if date and not is_valid_date(date): 
            messagebox.showerror(title="Invalid date", message="Invalid date. The date should be in the format dd-mm-yyyy")
            return
        # make a list of all the search entries that arent empty and
        # record which column they refer to - needed to search the databse
        queries = [[j, item.get()] for j, item in enumerate(self.patient_form.form_items.values()) if item.get()]
        results = self.db.search("patients", queries, strict=self.strict_search) # search if there are any patients that match the search
        if results: # there are results
            self.patient_table.set_row_count(len(results)) # set the table to hold any results
            for j, result in enumerate(results):
                self.patient_table.set_row(j, result)
        else:
            messagebox.showinfo(title="No results", message="Could not find any results for that query") # there were no results so let the user know. this avoids the table disappearing

    def save_patient(self):
        if not self.patient_form.completed_required(): # if the required items werent filled in
            messagebox.showerror(title="Error", message="Please fill in all nescessary entries (marked with *)")
            return
        # get the date and check if the date is valid
        date = self.patient_form.form_items["date_of_birth"].get() 
        if date and not is_valid_date(date):
            messagebox.showerror(title="Invalid date", message="Invalid date. The date should be in the format dd-mm-yyyy")
            return
        data = {} # data will hold each form item and what was entered
        for key, value in self.patient_form.form_items.items():
            if value.get():
                data[key] = value.get()

        if data.get("patient_id"): # if the patient id was entered then update the patients information
            # check if the patient id was a number
            try:
                data["patient_id"] = int(data.get("patient_id"))
            except Exception:
                messagebox.showerror(title="Error", message="Invalid Patient ID")
            else:
                # id was provided and the id was an integer
                messagebox.showinfo(title="Info", \
                                    message="Saved" if \
                                    self.db.update(
                                        data.get("patient_id"),
                                        "patients",
                                        [
                                            [
                                                self.db.column_indexes["patients"].get(column), # create a list of lists with each item and the column index
                                                data.get(column)
                                            ]
                                            for column in data.keys()
                                        ]
                                    )
                                    else "There was an error saving") # display saved if updating the information was a success else show there was an error
        else:
            # patient id was omitted -> make a new patient
            messagebox.showinfo(title="Info", message="New Patient with ID: " + str(self.db.insert(data, "patients"))) # the patient id was blank so create a new patient and let the user know of the new patient's id

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
            self.patient_form.set_all(result) # set the form to hold all of the patient's details

    def toggle_strict_search(self):
        # used when the checkbox is clicked to toggle strict searching
        self.strict_search = not self.strict_search
