from tkinter import *
from tkinter import messagebox
from DatabaseHandler import DB
from Admin import Admin
from DrNurse import DrNurse
from Therapist import Therapist
# class to contain login window
# __init__ gets passed the other menus that should open on a successful login
class Login(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title("Login")
        self.entry_username = Entry(self)
        
        self.entry_password = Entry(self, show='*')
        self.button_login = Button(self, text="Login", command=self.authenticate)

        # add all widgets to the screen
        self.entry_username.pack()
        self.entry_password.pack()
        self.button_login.pack()
        
        self.db = DB() # database handler to easily access the databse
    def authenticate(self):
        # gather the entered information
        username = self.entry_username.get()
        password = self.entry_password.get()
      
        login_result = self.db.login(username, password)
        # login result will return the type of account if the login was successful or an error message
        if login_result == "Invalid username or password": 
            messagebox.showerror(title="Error", message=login_result)
        else:
            # destory the current window becuase
            # a new window is being opened
            self.destroy()
            self.db.destroy()
            if login_result == "admin":
                Admin().mainloop()
            elif login_result == "doctor" or login_result == "nurse":
                DrNurse().mainloop()
            elif login_result == "therapist":
                Therapist(username).mainloop()
