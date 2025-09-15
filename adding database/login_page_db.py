'''this will be used as the login page.
all functions coded will be put here (GUI and back end python)'''
import customtkinter as ctk
from tkinter import messagebox
import subprocess
import sys
import sqlite3

from adding_database.shared_database import init_db, db_file

#Adding a main database
db_file = "diary_app.db"

class DatabaseManager:

    '''Handles all database interactions.'''

    def __init__(self, db_name="diary_app.db"):

        '''Initialising database manager with a database name 
        and makes sure the user table exists.'''
        
        self.db_name = db_name
        self.initialize_user_database()

    def initialize_user_database(self):

        '''Create the `users` table if it does not already exist.'''

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            """)
            conn.commit()

    def validate_user(self, username, password):

        '''Check if a user with the given username and password exists 
        in the database. Returns the user record if found, otherwise None.'''

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username FROM users WHERE username=? AND password=?", (username, password))
            return cursor.fetchone()

    def register_user(self, username, password):

        '''Insert a new user into the database. Raises an error if the 
        username already exists.'''

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()


class RegisterWindow:

    '''In charge of registration popup window.'''

    def __init__(self, parent, db_manager):

        '''Create a new popup window for registering users.'''

        self.parent = parent
        self.db_manager = db_manager
        self.create_window()

    def create_window(self):

        '''Build and display the registration popup GUI.'''

        self.popup = ctk.CTkToplevel(self.parent)
        self.popup.title("Register new user")
        self.popup.geometry("500x300")
        self.popup.configure(fg_color="#fffef8")
        self.popup.iconbitmap("images/logo.ico")

        #Centering registration window.
        window_width, window_height = 500, 300
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.popup.geometry(f"{window_width}x{window_height}+{x}+{y}")

        #Sign up GUI.
        ctk.CTkLabel(self.popup, text="SIGN UP",
                     font=("Helvetica", 24, "bold"),
                     fg_color="#fffef8", text_color="#7c5b44").place(relx=0.42, rely=0.16)

        self.username_entry = ctk.CTkEntry(self.popup, font=("Arial", 13),
                                           width=210, placeholder_text="Create Username",
                                           text_color="#7c5b44", fg_color="#fffef8")
        self.username_entry.place(relx=0.3, rely=0.4)

        self.password_entry = ctk.CTkEntry(self.popup, font=("Arial", 13),
                                           width=210, show="•",
                                           placeholder_text="Create Password",
                                           text_color="#7c5b44", fg_color="#fffef8")
        self.password_entry.place(relx=0.3, rely=0.57)

        #Password toggle.
        self.toggle_label = ctk.CTkLabel(self.popup, text="Show",
                                         text_color="#7c5b44", font=("Arial", 11, "underline"),
                                         cursor="hand2")
        self.toggle_label.place(relx=0.74, rely=0.57)
        self.toggle_label.bind("<Button-1>", lambda e: self.toggle_password())

        #Submit button.
        ctk.CTkButton(self.popup, text="Create New User",
                      command=self.save_new_user,
                      fg_color="#7c5b44", text_color="#fffef8",
                      hover_color="#b59a90", width=210).place(relx=0.3, rely=0.74)

    def toggle_password(self):
        
        '''Show or hide the password entered in the registration form.'''

        if self.password_entry.cget("show") == "•":
            self.password_entry.configure(show="")
            self.toggle_label.configure(text="Hide")
        else:
            self.password_entry.configure(show="•")
            self.toggle_label.configure(text="Show")

    def save_new_user(self):

        '''Validate registration form input and save the new 
        user into the database.'''

        reg_username = self.username_entry.get().strip()
        reg_password = self.password_entry.get().strip()

        if not reg_username or not reg_password:
            messagebox.showwarning("Validation Error", "Username and password cannot be empty.")
            return

        #Validate password.
        special_chars = "!@#$%^&*()}~`,.<>?/:;{[]|\+=™¡£¢∞§¶•ªºåœ∑´®†¥¨ˆøπåß∂ƒ©˙∆˚¬≈ç√∫˜µ≤≥"
        if len(reg_password) < 8:
            messagebox.showwarning("Validation Error", "Password must be at least 8 characters.")
            return
        if len(reg_password) > 20:
            messagebox.showwarning("Validation Error", "Password cannot be more than 20 characters.")
            return
        if not any(char in special_chars for char in reg_password):
            messagebox.showwarning("Validation Error", "Password must include at least one special character.")
            return

        #Save user to database.
        try:
            self.db_manager.register_user(reg_username, reg_password)
            messagebox.showinfo("Success", "User registered successfully!")
            self.popup.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists. Please choose another.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save user:\n{e}")


class LoginApp:

    '''Main login application.'''

    def __init__(self, root):

        '''Login application with the main root window and 
        a database manager.'''

        self.root = root
        self.db_manager = DatabaseManager()

        self.setup_ui()

    def setup_ui(self):

        '''Login page GUI'''

        self.root.title("Secret Self Diary App")
        self.root.geometry("1400x900")
        self.root.configure(fg_color="#fffef8")
        self.root.iconbitmap("images/logo.ico")

        #Welcome message.
        ctk.CTkLabel(self.root, text="Secret Self Diary App",
                     font=('Helvetica', 32), fg_color="#fffef8",
                     text_color="#7c5b44").place(relx=0.5, rely=0.1, anchor="center")

        #Login message.
        ctk.CTkLabel(self.root, text="LOGIN",
                     font=("Helvetica", 24, "bold"),
                     text_color="#7c5b44").place(relx=0.5, rely=0.16, anchor="center")

        #Username entry.
        self.username_entry = ctk.CTkEntry(self.root, font=("Arial", 13),
                                           width=300, placeholder_text="Username",
                                           text_color="#7c5b44", fg_color="#fffef8")
        self.username_entry.place(relx=0.4, rely=0.25)

        #Password entry.
        self.password_entry = ctk.CTkEntry(self.root, font=("Arial", 13),
                                           show="•", width=300,
                                           placeholder_text="Password",
                                           text_color="#7c5b44", fg_color="#fffef8")
        self.password_entry.place(relx=0.4, rely=0.33)

        #Login button.
        ctk.CTkButton(self.root, text="LOGIN",
                      command=self.enter_user_name,
                      fg_color="#7c5b44", text_color="#fffef8",
                      hover_color="#b59a90", width=300).place(relx=0.4, rely=0.4)

        #Signup button.
        signup_text = ctk.CTkLabel(self.root, text="Don't have an account? Sign up here",
                                   text_color="#7c5b44", cursor="hand2",
                                   font=("Arial", 12, "underline"))
        signup_text.place(relx=0.44, rely=0.45)
        signup_text.bind("<Button-1>", lambda e: RegisterWindow(self.root, self.db_manager))

    def enter_user_name(self):
        
        '''Validate login form input, check user credentials, 
        and continue if login is successful.'''

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Validation Error", "Username and password cannot be empty.")
            return

        #Validate password format.
        special_chars = "!@#$%^&*()}~`,.<>?/:;{[]|\+=™¡£¢∞§¶•ªºåœ∑´®†¥¨ˆøπåß∂ƒ©˙∆˚¬≈ç√∫˜µ≤≥"
        if len(password) < 8:
            messagebox.showwarning("Validation Error", "Password must be at least 8 characters.")
            return
        if len(password) > 20:
            messagebox.showwarning("Validation Error", "Password cannot be more than 20 characters.")
            return
        if not any(char in special_chars for char in password):
            messagebox.showwarning("Validation Error", "Password must include at least one special character.")
            return

        try:
            user = self.db_manager.validate_user(username, password)
            if not user:
                messagebox.showerror("Login Failed", "Invalid username or password.")
                return

            user_id, username = user
            messagebox.showinfo("Success", f"Thank you for logging in, {username}!")
            self.root.destroy()

            script_path = "/Users/maria/Desktop/13DDT/13DDT-PROG-MariaSecara/Secret Self Diary App/adding_database/daily_qs_db.py"
            subprocess.Popen([sys.executable, script_path, str(user_id)])

        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong, please try again:\n{e}")

#Running the program.
if __name__ == "__main__":
    root = ctk.CTk()
    app = LoginApp(root)
    root.mainloop()
