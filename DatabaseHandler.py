import sqlite3 as sql

class DB:
    def __init__(self):
        self.database = "databse.db"
        self.conn = sql.connect(self.database)
        self.cursor = self.conn.cursor()

#####################################
        '''
        must check that all the tables exist before being able to access them
        '''
        # users table
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS `users` (
                username PRIMARY KEY,
                password TEXT NOT NULL,
                type TEXT
            )
        ''')
        
        # tuple to index the columns specified when editing the databse
        self.patients_cols = ("patient_id", "name", "date_of_birth", "gender", "email", "phone", "post_code", "street", "house", "city")
        # patients table
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
                city TEXT NOT NULL
            )
        ''')

        # appointments table
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS `appointments` (
                appointment_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                patient_id INTEGER NOT NULL,
                practitioner TEXT NOT NULL,
                location TEXT
            )
        ''')
        self.conn.commit() # save to the database
##################################### 

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

    def update_patient(self, data):
        everything = self.get_all("patients") # get the entire table to search through and find the row that needs updating
        # delete the table
        self.cursor.execute(f'''
            DELETE FROM `patients`
        ''')
        for row in everything:
            row = list(row) # cast to a list to enable editing
            if row[0] == data.get("patient_id"):
                # found the patient
                for column, value in data.items():
                     # go through each column specified in the arguments and update the correct column
                    try:
                        # try and find what column the header is
                        index = self.patients_cols.index(column) 
                    except Exception:
                        # the column isnt valid
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
        return "Saved"

    def insert_row(self, table, values: tuple):
        self.cursor.execute(f'''
            INSERT OR IGNORE INTO `{table}`
            VALUES {values}
        ''')
        self.conn.commit() # save to the database
        return self.cursor.lastrowid

    def create_patient(self, data):
        # attempt to add the patient into the table
        # will ignore if the patient  already exists in the databse or
        # if another error occurs
        self.cursor.execute(f'''
            INSERT OR IGNORE INTO `patients`
            {tuple(data)}
            VALUES {tuple(data.values())}
        ''')
        self.conn.commit() # save to the database
        return f"Created Patient with ID: {self.cursor.lastrowid}"


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
        self.cursor.execute(f'''
            SELECT * FROM `{table}`
        ''')
        return self.cursor.fetchall()
        
    def destroy(self):
        self.conn.close()
