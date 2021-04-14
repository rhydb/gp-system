import sqlite3 as sql

class DB:
    def __init__(self):
        self.database = "databse.db"
        self.conn = sql.connect(self.database)
        self.cursor = self.conn.cursor()
        
        # users table
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS `users` (
                username PRIMARY KEY,
                password TEXT NOT NULL,
                type TEXT
            )
        ''')
        
        # patients table
        self.patient_form = [
            {
                "name": "patient_id",
                "display_name": "Patient ID",
                "type": "entry",
                "width": 5
            },
            {
                "name": "name",
                "display_name": "Name",
                "type": "entry",
                "required": True,
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
                "type": "dropdown",
                "menu_items": ["", "Male", "Female"],
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

        # appointments table
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

        # treatments table
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
                "type": "entry",
                "required": True
            },
            {
                "name": "cost",
                "display_name": "Cost",
                "type": "entry",
                "requred": True
            }
        ]
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS `treatments` (
                patient_id INTEGER,
                treatment TEXT NOT NULL,
                cost REAL NOT NULL
            )
        ''')

        # dictionary to store the index for each column for each table
        
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS `therapists` (
                patient_id INTEGER,
                username TEXT,
                record TEXT
            )
        ''')

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
        self.conn.commit() # save to the database

    def delete_row(self, table, row):
        everything = self.get_all(table)
        for i in range(row+1, len(everything)):
            # loop to shift everything after the specified row down to the left
            everything[i-1] = everything[i]
        everything.pop() # last two items are now the same so remove the last item from the array
        self.cursor.execute(f'''
            DELETE FROM `{table}`
        ''') # delete the old database
        for i in everything:
            # insert the updated rows back into the database
            self.cursor.execute(f'''
                INSERT INTO `{table}`
                VALUES {i}
            ''')
        self.conn.commit() # save to the database

    # a linear search to search for any matches
    # this is needed instead of a binary search as not all the data is sorted
    # and we need multiple results and to check multiple things at a time
    def search(self, table, params: list, strict=False):
        # basic check that all the items in the list are lists and contain two items
        # format to search: [column index, search value]
        for i in params:
            if type(i) is not list:
                raise Exception(f"Invalid search type '{type(i)}'")
            if len(i) != 2:
                raise Exception("Invalid format for search list")
        everything = self.get_all(table) # get everything in the table for searching
        # everything is eveything in the table which is
        # a list of tuples, each tuple is a row with each item in it
        # being the different column value
        results = []
        for row in everything:
            good = True
            for search in params:
                if strict:
                    if str(row[search[0]]) != str(search[1]): # strict search - they must match perfectly
                        good = False
                        break # check failed - no point checking the other columns
                else:
                    if str(search[1]) not in str(row[search[0]]): # more flexible search - the column simply has to contain the seartch (better for general searching)
                        good = False
                        break # check failed - no point checking the other columns
            if good:
                results.append(row) # good was never set to false so the row matches all of the searches
        return results
    
    # a recursive binary search to search for a specific patient using an id
    # since the id is the primary key and is sorted a binary search is appropiate
    # value is the search value and the value index is the column number the value is stored in. This is needed as binary search can only sort through one piece of data
    def b_search(self, value, value_index, table="", array=None, start=0, end=0, get_row_number=False):
        if array: # check if this is a recursive call or the first call
            if start > end: # when this occurs the list has been searched and the item is not in the list
                return
            mid = (end+start)//2 # the middle position
            if value == array[mid][value_index]:
                if get_row_number:
                    return mid # return the row number rather than the row
                return array[mid] # found the item
            if value > array[mid][value_index]:
                return self.b_search(value, value_index, array=array, start=mid+1, end=end, get_row_number=get_row_number) # the middle is less than the search, use the right half
            return self.b_search(value, value_index, array=array, start=start, end=mid-1, get_row_number=get_row_number) # the middle is greater than the search, use the left half
        # it is the first call, set up the paramaters and begin the search
        data = self.get_all(table)
        if data:
            return self.b_search(value, value_index, array=data, start=0, end=len(data)-1, get_row_number=get_row_number)
        return None
    
    def update_patient(self, data):
        found = False
        everything = self.get_all("patients") # get the entire table to search through and find the row that needs updating
        # delete the table
        self.cursor.execute(f'''
            DELETE FROM `patients`
        ''')
        for row in everything:
            row = list(row) # cast to a list to enable editing
            if row[0] == data.get("patient_id"):
                # found the patient
                found = True
                for column, value in data.items():
                    # try and find what column the header is
                    index = self.column_indexes.get(column)
                    if index is None: # failed to get the column - invalid
                        return f"Invalid column header: {column}"
                    else:
                        row[index] = value # update the column with the new value
            # set all None values to an emtpy string
            for i in range(len(row)):
                if row[i] is None:
                    row[i] = ""
                    
            # insert the row back into the table
            self.cursor.execute(f'''
                INSERT INTO `patients`
                VALUES {tuple(row)}
            ''')
        self.conn.commit() # save to the database
        return "Saved" if found else "Could not find that patient"

    def update(self, primary_key, table, values):
        row_number = self.b_search(primary_key, 0, table=table, get_row_number=True) # perform a binary search on the table to find which row it is
        if row_number is None:
            return False # failed to find the correct row in the table
        data = self.get_all(table)
        for index, value in values: # values is an array of 2-items array e.g: [[column_index, new_value]]
            data[row_number] = list(data[row_number]) # cast to list to allow editing
            data[row_number][index] = value

        # delete everything to re-add the updates row in the same place
        self.cursor.execute(f'''
            DELETE FROM `patients`
        ''')

        for row in data:
            self.cursor.execute(f'''
                INSERT INTO `{table}`
                VALUES ({",".join("?" * len(row))})
            ''', tuple(row))
        self.conn.commit()
        return True
        
    def update_unsorted(self, table, criteria: list, data: list, only_first=False):
        everything = self.get_all(table)
        for row in range(len(everything)):
            everything[row] = list(everything[row])
            good = True
            for item in criteria:
                if everything[row][item[0]] != item[1]:
                    good = False
                    break
            if good:
                for item in data:
                    everything[row][item[0]] = item[1]
                if only_first:
                    break
        self.cursor.execute(f'''
            DELETE FROM `{table}`
        ''')
        for row in everything:
            self.cursor.execute(f'''
                INSERT INTO `{table}`
                VALUES ({",".join("?" * len(row))})
            ''', tuple(row))
        self.conn.commit()
        
                

    def insert(self, data, table):
        # attempt to add the patient into the table
        # will ignore if the patient  already exists in the databse or
        # if another error occurs
        self.cursor.execute(f'''
            INSERT OR IGNORE INTO `{table}`
            {tuple(data)}
            VALUES ({",".join("?" * len(data.values()))})
        ''', tuple(data.values()))
        self.conn.commit() # save to the database
        return self.cursor.lastrowid

    def create_account(self, username, password, usertype):
        # attempt to add the user to the databse
        # will ignore if the user already exists in the databse or
        # if another error occurs
        self.cursor.execute(f'''
            INSERT OR IGNORE INTO `users`
            (username, password, type)
            VALUES (?, ?, ?)
        ''', (username, password, usertype))
        self.conn.commit() # save to the database
        return self.cursor.lastrowid

    def login(self, username, password):
        result = self.search("users", [[0, username], [1, password]], strict=True)
        if len(result) == 1: # result contains a row
            return result[0][2] # return the user type
        return "Invalid username or password" # invalid login

    def get_all(self, table):
        try:
            self.cursor.execute(f'''
                SELECT * FROM `{table}`
            ''')
        except Exception:
            return None
        return self.cursor.fetchall()
        
    def destroy(self):
        self.conn.close()
