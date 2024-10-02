import sqlite3
import tkinter as tk
from tkinter import messagebox
import tkinter.simpledialog as simpledialog
import time
import pyotp
import qrcode


class LoginApp:

    def __init__(self):
        self.login_window = tk.Tk()
        self.login_window.title('Login Application')
        self.login_window.geometry("650x250")

        key = "LoginAppSecretKeyKeyKey"

        tk.Label(self.login_window, text='Username').pack()
        self.username_entry = tk.Entry(self.login_window)
        self.username_entry.pack()

        tk.Label(self.login_window, text='Password').pack()
        self.password_entry = tk.Entry(self.login_window, show='*')
        self.password_entry.pack()

        self.login_button = tk.Button(self.login_window, text='Login', command=lambda: self.login(key))
        self.login_button.pack()

        self.create_button = tk.Button(self.login_window, text='Create Profile', command=self.create_profile)
        self.create_button.pack()

        self.login_window.mainloop()
    
    def login(self, key):

        print(key)

        conn = sqlite3.connect('user_db.db')
        cursor = conn.cursor()

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?;', (username, password))
        user = cursor.fetchone()

        if user:

            #Add ability to login without 2FA if not enabled, i.e database boolean for each account

            #Make it so the qr code is saved in the database and can be displayed in the app.

            totp = pyotp.TOTP(key, interval=30) #Fix key not generating correct code

            current_code = totp.now()
            print(f"Expected Code: {current_code}") 

            user_code = tk.simpledialog.askstring("2FA", "Enter 2FA Code: ")

            if user_code and totp.verify(user_code):

                self.show_profile(user, key)
                messagebox.showinfo('Success', 'Login Successful!')
            else:
                messagebox.showerror('Login Failed', 'Invalid 2FA code')
        else:
            messagebox.showerror('Login failed', 'Invalid username or password')
    
    def show_profile(self, user, key):
        self.login_window.destroy()
        self.profile_window = tk.Tk()
        self.profile_window.geometry("650x250")
        self.profile_window.title(f'Profile of {user[0]}')

        self.logout_button = tk.Button(self.profile_window, text='Log out', command=self.__init__)
        self.logout_button.pack()

        self.TwoFA_button = tk.Button(self.profile_window, text='Enable 2FA', command=lambda: self.initialise_2FA(key, user))
        self.TwoFA_button.pack()

        tk.Label(self.profile_window, text=f'Name: {user[2]}').pack()
        tk.Label(self.profile_window, text=f'Age: {user[3]}').pack()
        tk.Label(self.profile_window, text=f'E-Mail: {user[4]}').pack()

        self.profile_window.mainloop()

    def initialise_2FA(self, user, key):
        uri = pyotp.totp.TOTP(key).provisioning_uri(name=f"{user[0]}", issuer_name="Python LoginApp")
        qrcode.make(uri).save(f"{user[0]}_qrcode.png")
        messagebox.showinfo('Success', '2FA Enabled!')
    
    def create_profile(self):
        self.login_window.destroy()
        self.create_profile_window = tk.Tk()
        self.create_profile_window.geometry("650x450")
        self.create_profile_window.title('Create Profile')

        self.back_button = tk.Button(self.create_profile_window, text='Back', command=self.__init__)
        self.back_button.pack()

        tk.Label(self.create_profile_window, text='Username').pack()
        self.create_username_entry = tk.Entry(self.create_profile_window)
        self.create_username_entry.pack()

        tk.Label(self.create_profile_window, text='Password').pack()
        self.password1_entry = tk.Entry(self.create_profile_window, show='*')
        self.password1_entry.pack()

        tk.Label(self.create_profile_window, text='Confirm Password').pack()
        self.password2_entry = tk.Entry(self.create_profile_window)
        self.password2_entry.pack()

        tk.Label(self.create_profile_window, text='Name').pack()
        self.name_entry = tk.Entry(self.create_profile_window)
        self.name_entry.pack()

        tk.Label(self.create_profile_window, text='Age').pack()
        self.age_entry = tk.Entry(self.create_profile_window)
        self.age_entry.pack()

        tk.Label(self.create_profile_window, text='Email').pack()
        self.email_entry = tk.Entry(self.create_profile_window)
        self.email_entry.pack()

        self.login_button = tk.Button(self.create_profile_window, text='Create', command=self.add_profile)
        self.login_button.pack()

        self.create_profile_window.mainloop()

    def add_profile(self):

        conn = sqlite3.connect('user_db.db')
        cursor = conn.cursor()

        #Will add data validation logic within here

        add_username = self.create_username_entry.get()
        add_password = self.password1_entry.get()
        add_name = self.name_entry.get()
        add_age = self.age_entry.get()
        add_email = self.email_entry.get()

        if True:

            cursor.execute('INSERT INTO users (username, password, name, age, email) VALUES (?, ?, ?, ?, ?)', (add_username, add_password, add_name, add_age, add_email))

            messagebox.showinfo('Success', 'Account creation successful!')
            
            self.create_profile_window.destroy()
            self.__init__()
        else :
            messagebox.showerror('Account creation failed', 'Invalid input')
        
        conn.commit()
        conn.close()



if __name__ == '__main__':
    LoginApp()