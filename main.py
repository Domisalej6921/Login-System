import sqlite3
import tkinter as tk
from tkinter import messagebox


class LoginApp:

    def __init__(self):
        self.login_window = tk.Tk()
        self.login_window.title('Login Application')
        self.login_window.geometry("650x250")

        tk.Label(self.login_window, text='Username').pack()
        self.username_entry = tk.Entry(self.login_window)
        self.username_entry.pack()

        tk.Label(self.login_window, text='Password').pack()
        self.password_entry = tk.Entry(self.login_window, show='*')
        self.password_entry.pack()

        self.login_button = tk.Button(self.login_window, text='Login', command=self.login)
        self.login_button.pack()

        self.create_button = tk.Button(self.login_window, text='Create Profile', command=self.create_profile)
        self.create_button.pack()

        self.login_window.mainloop()
    
    def login(self):
        conn = sqlite3.connect('user_db.db')
        cursor = conn.cursor()

        username = self.username_entry.get()
        password = self.password_entry.get()

        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?;', (username, password))
        user = cursor.fetchone()

        if user:
            self.show_profile(user)
        else:
            messagebox.showerror('Login failed', 'Invalid username or password')

        conn.close()
    
    def show_profile(self, user):
        self.login_window.destroy()
        self.profile_window = tk.Tk()
        self.profile_window.geometry("650x250")
        self.profile_window.title(f'Profile of {user[0]}')

        self.logout_button = tk.Button(self.profile_window, text='Log out', command=self.__init__)
        self.logout_button.pack()

        tk.Label(self.profile_window, text=f'Name: {user[2]}').pack()
        tk.Label(self.profile_window, text=f'Age: {user[3]}').pack()
        tk.Label(self.profile_window, text=f'E-Mail: {user[4]}').pack()

        self.profile_window.mainloop()
    
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
            messagebox.showinfo('Success', 'Account creation successful!')

            cursor.execute('INSERT INTO users (username, password, name, age, email) VALUES (?, ?, ?, ?, ?)', (add_username, add_password, add_name, add_age, add_email))
            
            self.create_profile_window.destroy()
            self.__init__()
        else :
            messagebox.showerror('Account creation failed', 'Invalid input')
        
        conn.commit()
        conn.close()



if __name__ == '__main__':
    LoginApp()