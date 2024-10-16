# Login-System
This is the source code for my login system project.

In the test_data file there is the sample data which can be used for logging in. User1 has 2fa so you will be unable to access his account unless you have the right 2FA code (Try it!). If you have troubles with the database, delete it and run the create_db.py file and that will give you a fresh copy of the database.

In the database the column "two_factor_auth" works by setting 0 as the default value (Disabled) and 1 if you have enabled 2FA.

------------------------------------------------------------------------------------------------------------------------

What I have implemented already:

- Program checks if user is in the database.
- User can create an account through the program.
- User can navigate through GUI pages in the program.
- Seperate account dashboard for each user.
- 2FA.
- A well designed, visually appealing GUI.
- Data Validation
- Password Hashing + Salting

------------------------------------------------------------------------------------------------------------------------

What features I would like to implement:

- Some cryptography elements.
- Eliminate possible vulnerabilities such as SQL Injection, etc.
- Add the ability to show the qr code in the app and store it in the database securely.