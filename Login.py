from tkinter import *
from tkinter import messagebox
from DatabaseHandler import DB # DB is a class that allows for easy interaction with the database
# these are the other pages that can open after loggin in
from Admin import Admin
from DrNurse import DrNurse
from Therapist import Therapist
# class for the login window
# handles authentication and opening the correct window based on who loggged in
class Login(Tk): # a class to contain all widgets in the menu, inherits from the Tk object
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs) # create the Tk object that this inherits from
        self.title("Login")

        # the three widegets on the form used to login
        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show='*')
        self.button_login = Button(self, text="Login", command=self.authenticate) # when clicked -> check the credentials and login

        # add all widgets to the screen
        self.entry_username.pack()
        self.entry_password.pack()
        self.button_login.pack()
        
        self.db = DB() # database handler that connects to the database file

    
    # called by clicking button_login
    # it calls the login method on the database handler and handles the result
    def authenticate(self):
        # gather the entered information from the entry boxes
        username = self.entry_username.get()
        password = self.entry_password.get()

        login_result = self.db.login(username, password) # call the login method on the database handler which interacts with the databsae
        # login result will return the type of account if the login was successful or an error message
        if login_result == "Invalid username or password": # the error message that the database returns on an invalid login 
            messagebox.showerror(title="Error", message=login_result)
        else:
            self.destroy() # destory the current window becuase a new window is being opened
            self.db.destroy() # close the connection to the database
            # start the appropiate window based on the user type that was returned from logging in
            if login_result == "admin":
                Admin().mainloop()
            elif login_result == "doctor" or login_result == "nurse":
                DrNurse().mainloop()
            elif login_result == "therapist":
                Therapist(username).mainloop() # Therapist takes a username which is passed here
