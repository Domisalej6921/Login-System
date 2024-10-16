import sqlite3
import tkinter as tk
import customtkinter
from tkinter import messagebox
import base64
import tkinter.simpledialog as simpledialog
import pyotp
import qrcode
import re
import bcrypt


class LoginApp:

    def __init__(self):

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        key = "LoginAppSecretKeyKeyKey"
        key = base64.b32encode(key.encode())
        key = key.decode()

        salt = bcrypt.gensalt(rounds=12)

        self.login_window(key, salt)
    
    def login_window(self, key, salt):
        self.login_window = customtkinter.CTk()
        self.login_window.title('Login Application')
        self.login_window.geometry("650x350")

        frame = customtkinter.CTkFrame(master=self.login_window)
        frame.pack(pady=20, padx=60, fill="both", expand=True)

        title_label = customtkinter.CTkLabel(master=frame, text="Login Application", font=("Roboto", 24))
        title_label.pack(pady=12, padx=10)

        self.username_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
        self.username_entry.pack(pady=12, padx=10)

        self.password_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show='*')
        self.password_entry.pack(pady=12, padx=10)

        self.login_button = customtkinter.CTkButton(master=frame, text='Login', command=lambda: self.login(key))
        self.login_button.pack(pady=12, padx=10)

        self.create_button = customtkinter.CTkButton(master=frame, text='Create Profile', command=lambda: self.create_profile(salt))
        self.create_button.pack(pady=12, padx=10)

        self.login_window.mainloop()
    
    def login(self, key):

        conn = sqlite3.connect('user_db.db')
        cursor = conn.cursor()

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        #fetch user
        cursor.execute('SELECT * FROM users WHERE username = ?;', (username,))
        user = cursor.fetchone()

        #If user exists
        if user:
            hashed_password = user[1]
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                #If user has enabled 2fa
                if user[5] == 1:

                    #Make it so the qr code is saved in the database and can be displayed in the app.

                    totp = pyotp.TOTP(key, interval=30)

                    user_code = tk.simpledialog.askstring("2FA", "Enter 2FA Code: ")

                    #validate user input
                    try:
                        user_code = int(user_code)
                    except ValueError:
                        messagebox.showerror('Login Failed', 'Invalid code format. Please enter numbers only.')
                        exit()

                    #verify 2fa codes are the same
                    if totp.verify(user_code, valid_window=1):
                        messagebox.showinfo('Success', 'Login Successful!')
                        self.show_profile(user, key)
                    else:
                        messagebox.showerror('Login Failed', 'Invalid 2FA code')
            
                #If user has not enabled 2fa
                elif user[5] == 0:
                    messagebox.showinfo('Success', 'Login Successful!')
                    self.show_profile(user, key)
                
                else:
                    messagebox.showerror('Login failed', 'Invalid 2FA type')

            #Hashed password isn't in database
            else:
                messagebox.showerror('Login failed', 'Password isn\'t on our system ')
        
        #If user has entered incorrect details
        else:
            messagebox.showerror('Login failed', 'User does not exist')
    
    def show_profile(self, user, key):
        self.login_window.quit()
        self.profile_window = customtkinter.CTk()
        self.profile_window.geometry("650x450")
        self.profile_window.title(f'Profile of {user[0]}')

        frame = customtkinter.CTkFrame(master=self.profile_window)
        frame.pack(pady=20, padx=60, fill="both", expand=True)

        profile_page_title = customtkinter.CTkLabel(master=frame, text='Account Dashboard', font=("Roboto", 24))
        profile_page_title.pack(pady=12, padx=10)

        self.logout_button = customtkinter.CTkButton(master=frame, text='Log out', command=self.logout)
        self.logout_button.pack(pady=12, padx=10)

        self.TwoFA_button = customtkinter.CTkButton(master=frame, text='Enable 2FA', command=lambda: self.initialise_2FA(key, user))
        self.TwoFA_button.pack(pady=12, padx=10)

        self.Disable_TwoFA_button = customtkinter.CTkButton(master=frame, text='Disable 2FA', command=lambda: self.disable_2fa(user))
        self.Disable_TwoFA_button.pack(pady=12, padx=10)

        customtkinter.CTkLabel(master=frame, text=f'Name: {user[2]}').pack(pady=12, padx=10)
        customtkinter.CTkLabel(master=frame, text=f'Age: {user[3]}').pack(pady=12, padx=10)
        customtkinter.CTkLabel(master=frame, text=f'E-Mail: {user[4]}').pack(pady=12, padx=10)

        self.profile_window.mainloop()

    def logout(self):
        self.profile_window.quit()

    def initialise_2FA(self, key, user):

        #Creates qr code stored locally for user to enable 2fa
        uri = pyotp.totp.TOTP(key).provisioning_uri(name=f"{user[0]}", issuer_name="Python LoginApp")
        qrcode.make(uri).save(f"{user[0]}_qrcode.png")

        #Updating the 2fa column in the user table
        conn = sqlite3.connect('user_db.db')
        cursor = conn.cursor()

        cursor.execute('UPDATE users SET two_factor_auth = ? WHERE username = ?', (1, user[0]))
        
        conn.commit()
        conn.close()

        #Show Success Message
        messagebox.showinfo('Success', '2FA Enabled!\nA QR code is stored locally on your computer.\nUse this for setup with your authenticator app.')

    def disable_2fa(self, user):
        #Reverting the 2fa column in the user table
        conn = sqlite3.connect('user_db.db')
        cursor = conn.cursor()

        cursor.execute('UPDATE users SET two_factor_auth = ? WHERE username = ?', (0, user[0]))
        
        conn.commit()
        conn.close()

        #Show Success Message
        messagebox.showinfo('Success', '2FA Disabled!')
    
    def create_profile(self, salt):
        self.login_window.quit()
        self.create_profile_window = customtkinter.CTk()
        self.create_profile_window.geometry("650x550")
        self.create_profile_window.title('Create Profile')

        frame = customtkinter.CTkFrame(master=self.create_profile_window)
        frame.pack(pady=20, padx=60, fill="both", expand=True)

        create_profile_page_title = customtkinter.CTkLabel(master=frame, text="Create An Account", font=("Roboto", 24))
        create_profile_page_title.pack(pady=12, padx=10)

        self.back_button = customtkinter.CTkButton(master=frame, text='Back', command=self.login_window)
        self.back_button.pack(pady=12, padx=10)

        self.create_username_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Username")
        self.create_username_entry.pack(pady=12, padx=10)

        self.password1_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show='*')
        self.password1_entry.pack(pady=12, padx=10)

        self.password2_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Confirm Password", show='*')
        self.password2_entry.pack(pady=12, padx=10)

        self.name_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Name")
        self.name_entry.pack(pady=12, padx=10)

        self.age_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Age")
        self.age_entry.pack(pady=12, padx=10)

        self.email_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Email")
        self.email_entry.pack(pady=12, padx=10)

        self.login_button = customtkinter.CTkButton(master=frame, text='Create', command=lambda: self.add_profile(salt))
        self.login_button.pack(pady=12, padx=10)

        self.create_profile_window.mainloop()

    def add_profile(self, salt):

        conn = sqlite3.connect('user_db.db')
        cursor = conn.cursor()
        
        add_username = self.create_username_entry.get()
        add_password = self.password1_entry.get()
        confirm_password = self.password2_entry.get()
        add_name = self.name_entry.get()
        add_age = self.age_entry.get()
        add_email = self.email_entry.get()

        # Default two_fa state is false
        two_fa = 0

        # Validate inputs
        if not self.validate_username(add_username):
            messagebox.showerror('Account creation failed', 'Invalid username format. Must be 3-20 characters and alphanumeric.')
            return
        if not self.validate_password(add_password):
            messagebox.showerror('Account creation failed', 'Invalid password format. Must be at least 8 characters long and include letters and numbers.')
            return
        if add_password != confirm_password:
            messagebox.showerror('Account creation failed', 'Passwords do not match!')
            return
        if not self.validate_name(add_name):
            messagebox.showerror('Account creation failed', 'Invalid name format. Name must contain only letters.')
            return
        if not self.validate_age(add_age):
            messagebox.showerror('Account creation failed', 'Invalid age format. Age must be a number between 1 and 120.')
            return
        if not self.validate_email(add_email):
            messagebox.showerror('Account creation failed', 'Invalid email format.')
            return

        # Hash the password before saving it to the database
        hashed_password = bcrypt.hashpw(add_password.encode('utf-8'), salt)

        cursor.execute('INSERT INTO users (username, password, name, age, email, two_factor_auth) VALUES (?, ?, ?, ?, ?, ?)', (add_username, hashed_password, add_name, add_age, add_email, two_fa))

        conn.commit()
        conn.close()

        messagebox.showinfo('Success', 'Account creation successful!')
        
        self.create_profile_window.quit()

    #Validation functions
    def validate_username(self, username):
        return bool(re.match(r'^[A-Za-z0-9]{3,20}$', username))
    
    def validate_password(self, password):
        return len(password) >= 8 and re.search(r'[A-Za-z]', password) and re.search(r'[0-9]', password)
    
    def validate_name(self, name):
        return bool(re.match(r'^[A-Za-z\s]+$', name))
    
    def validate_age(self, age):
        return age.isdigit() and 1 <= int(age) <= 120
    
    def validate_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, email))


if __name__ == '__main__':
    LoginApp()