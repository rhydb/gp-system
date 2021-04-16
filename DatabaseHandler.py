import sqlite3 as sql

class DB:
    def __init__(self):
        self.database = "databse.db" # the sql database file
        self.conn = sql.connect(self.database) # create an sql connection to database file, creates it if it doesnt exist
        self.cursor = self.conn.cursor() # create a cursor off the connection
        
        # create the users table if it doesnt exist already
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS `users` (
                username PRIMARY KEY,
                password TEXT NOT NULL,
                type TEXT
            )
        ''')
        
        # the form that is used to create and search for patients
        # it gets fed into Form.py to create a Tkinter form
        # this makes it easier to change and add things
        # it also contains the names of the column that it represents in the database
        self.patient_form = [
            {
                "name": "patient_id",
                "display_name": "Patient ID",
                "type": "entry", # creates an Entry widget
                "width": 5 # width is the width of the entry box in characters
            },
            {
                "name": "name",
                "display_name": "Name",
                "type": "entry",
                "required": True, # required fields will have * appended and must be filled in before submitting the form
                "width": 15
            },
            {
                "name": "date_of_birth",
                "display_name": "Date of Birth\n(dd-mm-yyyy)",
                "type": "entry",
                "required": True,
                "width": 10
            },
            {
                "name": "gender",
                "display_name": "Gender",
                "required": True,
                "type": "dropdown", # dropdowns creates an OptionMenu widget
                "menu_items": ["", "Male", "Female"], # the options that the dropdown will contain
                "width": 6
            },
            {
                "name": "email",
                "display_name": "E-Mail",
                "type": "entry",
                "width": 15
            },
            {
                "name": "phone",
                "display_name": "Phone",
                "type": "entry",
                "width": 11
            },
            {
                "name": "post_code",
                "display_name": "Post Code",
                "required": True,
                "type": "entry",
                "width": 7
            },
            {
                "name": "street",
                "display_name": "Street",
                "required": True,
                "type": "entry",
                "width": 15
            },
            {
                "name": "house",
                "display_name": "House",
                "required": True,
                "type": "entry",
                "width": 10
            },
            {
                "name": "city",
                "display_name": "City",
                "required": True,
                "type": "entry",
                "width": 10
            }
        ]

        # create the patients table if it doesnt already exist
        # the patient id is the main id for the entire databse and is used as a foreign key in other tables
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS `patients` (
                patient_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name TEXT NOT NULL,
                date_of_birth DATE NOT NULL,
                gender TEXT,
                email TEXT,
                phone TEXT,
                post_code TEXT NOT NULL,
                street TEXT NOT NULL,
                house TEXT NOT NULL,
                city TEXT NOT NULL,
                history TEXT,
                details TEXT,
                referals TEXT,
                tests TEXT
            )
        ''')

        # creates the appointments table if it doesnt already exist
        # the patient id is a foreign key to the patients table
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS `appointments` (
                appointment_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                patient_id INTEGER NOT NULL,
                practitioner TEXT NOT NULL,
                location TEXT NOT NULL,
                date DATE NOT NULL,
                time INT NOT NULL
            )
        ''')
        # the form for creating a searching for appointments
        self.appointment_form = [
            {
                "name": "appointment_id",
                "display_name": "Appointment ID",
                "type": "entry",
                "width": 4
            },
            {
                "name": "patient_id",
                "display_name": "Patient ID",
                "type": "entry",
                "required": True,
                "width": 4
            },
            {
                "name": "practitioner",
                "display_name": "Practitioner",
                "type": "dropdown",
                "menu_items": ["", "Doctor/Nurse", "Therapist"],
                "required": True,
                "width": 12
            },
            {
                "name": "location",
                "display_name": "Location",
                "type": "dropdown",
                "menu_items": ["", "On-site", "On-line"],
                "required": True,
                "width": 7
            },
            {
                "name": "date",
                "display_name": "Date\n(dd-mm-yyyy)",
                "type": "entry",
                "required": True,
                "width": 10
            },
            {
                "name": "time",
                "display_name": "Time",
                "type": "entry",
                "required": True,
                "width": 2
            }
            
        ]
        
        # creates the treatments table if it doesnt already exist
        # patient id is a foreign key to the patients table
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS `treatments` (
                patient_id INTEGER,
                treatment TEXT NOT NULL,
                cost REAL NOT NULL
            )
        ''')
        # the form used to add treatments for a patient
        self.treatments_form = [
            {
                "name": "patient_id",
                "display_name": "Patient ID",
                "type": "entry",
                "required": True
            },
            {
                "name": "treatment",
                "display_name": "Treatment",
                "type": "dropdown",
                "menu_items": ["", "Acupuncture", "Nutrition"], # this is where any new therapy treatments can be added in the future
                "required": True
            },
            {
                "name": "cost",
                "display_name": "Cost",
                "type": "entry",
                "requred": True
            }
        ]
        
       

        # create thte table to hold information for patients to therapists
        # as different therapists must not have access to other data
        # the patient id is a foreign key to the patients table
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS `therapists` (
                patient_id INTEGER,
                username TEXT,
                record TEXT
            )
        ''')

        # these are used to store the different columns in each table and their corresponding column number
        # this is needed as storing data elsewhere is done through the name of the column rather than the column number
        # and is better than performing a search on each access
        self.column_indexes = {
            "patients": {
                "patient_id": 0,
                "name": 1,
                "date_of_birth": 2,
                "gender": 3,
                "email": 4,
                "phone": 5,
                "post_code": 6,
                "street": 7,
                "house": 8,
                "city": 9,
                "history": 10,
                "details": 11,
                "referals": 12,
                "tests": 13
            },
            "appointments": {
                "appointment_id": 0,
                "patient_id": 1,
                "pracitioner": 2,
                "location": 3,
                "date": 4,
                "time": 5
            },
            "treatments": {
                "patient_id": 0,
                "treatment": 1,
                "cost": 2
            },
            "therapists": {
                "patient_id": 0,
                "username": 1,
                "records": 2
            }
        }
         
        # create some default users to be able to log in to
        self.cursor.execute(f'''
            INSERT OR IGNORE INTO users
            VALUES ('admin', 'admin', 'admin')
        ''') 
        self.cursor.execute(f'''
            INSERT OR IGNORE INTO users
            VALUES ('dr', 'dr', 'doctor')
        ''')
        self.cursor.execute(f'''
            INSERT OR IGNORE INTO users
            VALUES ('therapist', 'therapist', 'therapist')
        ''')
        self.conn.commit() # save all (if any) changes to the database file

    # method to remove a row from a table with a row number
    def delete_row(self, table, row):
        everything = self.get_all(table) # get everything in the table to be able to manipulate it
        for i in range(row+1, len(everything)): 
            # go through each row after the specified row and shift it to the left 
            # this overwrites the desired row and deletes it
            everything[i-1] = everything[i] 
        everything.pop() # array has no shrunk by 1 so remove the last item

        # the table has been modified so remove the old table
        self.cursor.execute(f'''
            DELETE FROM `{table}`
        ''')
        for i in everything:
            # insert the updated rows back into the database but without the row that was deleted
            self.cursor.execute(f'''
                INSERT INTO `{table}`
                VALUES {i}
            ''')
        self.conn.commit() # save to the database file

    # a linear search to search for any matches in a table
    # this is needed instead of a binary search as not all the data is sorted
    # and this enables multiple colums to be searched against
    def search(self, table, params: list, strict=False):
        # basic check that all the items in the list are lists and contain two items
        # params should be in this format: [[column index, search value], ...]
        for i in params:
            # go through each item in params
            if type(i) is not list: # if it is not a list throw an error
                raise Exception(f"Invalid search type '{type(i)}'")
            if len(i) != 2: # if the list does not contain two items it is invalid, throw an error
                raise Exception("Invalid format for search list")
        # params is in a valid format so procede
        everything = self.get_all(table) # get everything in the table for searching
        # everything is a list of tuples, each tuple is a row with each item in it
        # being the different column value
        results = [] # to store any matching rows
        for row in everything:
            for search in params:
                if strict:
                    if str(row[search[0]]) != str(search[1]): # strict search - they must match perfectly
                        break # check failed - no point checking the other columns
                else:
                    if str(search[1]) not in str(row[search[0]]): # more flexible search - the column simply has to contain the seartch (better for general searching)
                        break # check failed - no point checking the other columns
            else:
                results.append(row) # break was never called so the row matches all of the searches, so append it to results
        return results # return the list with any matches
    
    # a recursive binary search to search for a specific row using a sorted value
    # since the value is sorted a binary search is appropiate
    # value is the search value and the value index is the column number the value is stored in.
    # instead of crreating copies of parts of the array it operates using indexes that will change and will allow for indexing in the original list
    def b_search(self, value, value_index, table="", array=None, start=0, end=0, get_row_number=False):
        if array: # check if this is a recursive call or the first call
            if start > end: # when this occurs the list has been searched and the item is not in the list
                return
            mid = (end+start)//2 # the position between the start and end of the unsearched portion of the list
            if value == array[mid][value_index]: # found a match
                if get_row_number:
                    # get_row_number will be set to True if trying to find the row number
                    # for example getting the row number for a row needed to be deleted
                    return mid # return the row number the match was found in 
                return array[mid] # return the row that a match was found in
            if value > array[mid][value_index]: # the search value is greater than the middle value so split the list again and search on the right half
                return self.b_search(value, value_index, array=array, start=mid+1, end=end, get_row_number=get_row_number)
            # if the search value was not equal or bigger then it is smaller
            # split the list in half and search the left side of the array
            return self.b_search(value, value_index, array=array, start=start, end=mid-1, get_row_number=get_row_number)
        # it is the first call, set up the paramaters and begin the search
        data = self.get_all(table)
        if data: # found some data
            return self.b_search(value, value_index, array=data, start=0, end=len(data)-1, get_row_number=get_row_number)
        return None # return None instead of an empty array to avoid too much recursion
    
    # a method to update a row in a sorted table using the primary key in a binary search
    # will return True/False on success/failure
    def update(self, primary_key, table, values): # values will be a 2D list in the format [[column index, new value]]
        row_number = self.b_search(primary_key, 0, table=table, get_row_number=True) # perform a binary search on the table to find which row it is
        if row_number is None: # b_search will return None if it cannot find the row
            return False # failed to find the correct row in the table
        data = self.get_all(table) # get all the rows in the table
        for index, value in values: # values is an array of 2-items array e.g: [[column_index, new_value]]
            data[row_number] = list(data[row_number]) # cast from tuple to list to allow item assignment
            data[row_number][index] = value # update the row's column with the new value using the column index

        # delete everything to re-add the updates row in the same place
        self.cursor.execute(f'''
            DELETE FROM `patients`
        ''')

        for row in data:
            self.cursor.execute(f'''
                INSERT INTO `{table}`
                VALUES ({",".join("?" * len(row))})
            ''', tuple(row)) # row must be a tuple to be inserted again
        self.conn.commit() # save changes to the databsae file
        return True # successfully updated the table
    
    # a method to update a row in a table if the table is not sorted, meaning the method above would not work because it uses a binary search
    # criteria is a 2D list to find matching rows in the format [[column index, search value], ...]
    # data is a 2D list that stores the new values for any row that matches the critera in the format [[column index, new value], ...]
    # onyl_first allows for only editing the first match, if left at false it will update all matches found rather than just the first
    def update_unsorted(self, table, criteria: list, data: list, only_first=False):
        everything = self.get_all(table) # get every row in the table
        for row in range(len(everything)): # for each row number in the table
            for item in criteria:
                if everything[row][item[0]] != item[1]:
                    break
            else: # break was never called so the row matches the criteria
                for item in data: # for column index - value pair
                    everything[row] = list(everything[row]) # cast from a tuple to a list to allow item assignment
                    everything[row][item[0]] = item[1] # set the column to the new value
                if only_first: # if only_first is True stop updating any other rows
                    break
        # remove the rows in the table as they have been updated
        self.cursor.execute(f'''
            DELETE FROM `{table}`
        ''')
        for row in everything: # add the updated rows back in
            self.cursor.execute(f'''
                INSERT INTO `{table}`
                VALUES ({",".join("?" * len(row))})
            ''', tuple(row)) 
            # ",".join("?" * len(row)) will add as many ?'s seprerated with , as needed. They are used to safely add values into a table
            # each row must be a tuple when inserting so cast to a tuple if it was edited
        self.conn.commit() # save changes to the database file
        
    def insert(self, data, table):
        # attempt to add the patient into the table
        # will ignore if the patient  already exists in the databse or
        # if another error occurs
        # data is a dictionairy with each column name and the value for the column
        self.cursor.execute(f'''
            INSERT OR IGNORE INTO `{table}`
            {tuple(data)}
            VALUES ({",".join("?" * len(data.values()))})
        ''', tuple(data.values()))
        # tuple(data) will cast all keys in data to a tuple, this is what sql needs to insert
        # ",".join("?" * len(data.values())) will add as many ?'s seprerated with , as needed. They are used to safely add values into a table
        # tuple(data.values()) will cast all the values in the dicitonairy to a tuple, it will be in the same order as the keys above it
        self.conn.commit() # save to the database file
        return self.cursor.lastrowid # return the primary key / row id of the new row

    def create_account(self, username, password, usertype):
        # attempt to add the user to the databse
        # will ignore if the user already exists in the databse or
        # if another error occurs
        self.cursor.execute(f'''
            INSERT OR IGNORE INTO `users`
            (username, password, type)
            VALUES (?, ?, ?)
        ''', (username, password, usertype))
        self.conn.commit() # save to the database file
        return self.cursor.lastrowid

    def login(self, username, password):
        result = self.search("users", [[0, username], [1, password]], strict=True) # perform a search on the users table using the username and password, it must be strict as they must match exactly
        if len(result) == 1: # result contains a row
            return result[0][2] # return the user type
        return "Invalid username or password" # invalid login

    def get_all(self, table): # a method to simply return the entire table
        try:
            self.cursor.execute(f'''
                SELECT * FROM `{table}`
            ''')
        except Exception:
            return None # something went wrong, catch it and return None
        return self.cursor.fetchall() # return all the results
    
    # close the connection to the database
    def destroy(self):
        self.conn.close()
