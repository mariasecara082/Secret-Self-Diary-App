'''this will be used as the login page.
all functions coded will be put here (GUI and back end python)'''
import customtkinter as ctk
from tkinter import messagebox
import subprocess
import sys
import sqlite3

#Initializing database
def initialize_user_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

#Here, I am starting to code the GUI for the login page.
def enter_user_name():

    '''main function (on the login page)
    in which the user enters their username and password'''
    
    username = user_name.get().strip() #.strip() is used to remove any trailing whitespaces (spaces, tabs, new lines)
    password = user_password.get().strip()

    # Check for empty fields.
    if not username or not password:
        messagebox.showwarning("Validation Error", "Username and password cannot be empty.")
        return

    #Checking password validity.
    special_chars = "!@#$%^&*()}~`,.<>?/:;{[]|\+=™¡£¢∞§¶•ªºåœ∑´®†¥¨ˆøπåß∂ƒ©˙∆˚¬≈ç√∫˜µ≤≥"
    if len(password) < 8: #Password length
        messagebox.showwarning("Validation Error", "Password must be at least 8 characters.")
        return
    if len(password) > 20: #Password length
        messagebox.showwarning("Validation Error", "Password cannot be more than 20 characters.")
        return
    if not any(char in special_chars for char in password): #Special characters.
        messagebox.showwarning("Validation Error", "Password must include at least one special character (!@#$%^&*()).")
        return
    
    #Check credentials in the database
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if not user:
            messagebox.showerror("Login Failed", "Invalid username or password.")
            return

        # Login successful
        messagebox.showinfo("Success", f"Thank you for logging in, {username}!")
        root.destroy()
        script_path = "/Users/maria/Desktop/13DDT/13DDT-PROG-MariaSecara/Secret Self Diary App/adding database/daily_qs_db.py"
        subprocess.Popen([sys.executable, script_path])

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong, please try again:\n{e}")

def createnew_popup():

    '''this creates a new pop-up window when the button
    to register a new user is pressed. the window
    has certain dimensions, just like the root'''

    popupwindow = ctk.CTkToplevel(root)
    popupwindow.title("Register new user")
    popupwindow.geometry("500x300")
    popupwindow.configure(fg_color="#fffef8")
    popupwindow.iconbitmap("images/logo.ico")

    window_width, window_height = 800, 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    popupwindow.geometry(f"{window_width}x{window_height}+{x}+{y}")

    #Label
    ctk.CTkLabel(popupwindow, 
                 text="SIGN UP", 
                 font=("Helvetica", 24, "bold"), 
                 fg_color="#fffef8", 
                 text_color="#7c5b44").place(relx=0.42, rely=0.16)

    register_username_entry = ctk.CTkEntry(popupwindow,
                             font=("Arial", 13),  
                             width=210, 
                             placeholder_text="Create Username", 
                             text_color="#7c5b44", 
                             fg_color="#fffef8")
    register_username_entry.place(relx=0.3, rely=0.4)

    register_password_entry = ctk.CTkEntry(popupwindow,
                             font=("Arial", 13),  
                             width=210, 
                             placeholder_text="Create Password", 
                             text_color="#7c5b44", 
                             fg_color="#fffef8")
    register_password_entry.place(relx=0.3, rely=0.57)

    def save_new_user(): 

        '''this function is made to save 
        the new registered user into the database, which
        will then be read and saved and can later be used for the login into
        the app.'''

        reg_username = register_username_entry.get().strip()
        reg_password = register_password_entry.get().strip()

        #If the password or username is left empty.
        if not reg_username or not reg_password:
            messagebox.showwarning("Validation Error", "Username and password cannot be empty.")
            return
        
        #Checking validity of the password
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
        
        #Saving the new registrated user into the database
        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (reg_username, reg_password))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "User registered successfully!")
            popupwindow.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists. Please choose another.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save user:\n{e}")

    ctk.CTkButton(popupwindow, 
                  text="Create New User", 
                  command=save_new_user, 
                  fg_color="#7c5b44", text_color="#fffef8", hover_color="#b59a90",
                  width=210).place(relx=0.3, rely=0.74)

    
    #new_user = new_user_name.get().strip()


#Creating a main window using root = tk.Tk().
root = ctk.CTk()
root.title("Secret Self Diary App")
root.geometry("1400x900")
root.configure(fg_color="#fffef8") #Making the root colour have a background colour.
root.iconbitmap("images/logo.ico")

#Welcome message displayed at the top of the root.
welcome_message = ctk.CTkLabel(root, text="Secret Self Diary App", font=('Helvetica', 32), fg_color="#fffef8", text_color="#7c5b44")
welcome_message.place(relx=0.5, rely=0.1, anchor="center")

#Login message below the welcome message
login_message = ctk.CTkLabel(root, text="LOGIN", font=("Helvetica", 24, "bold"), text_color="#7c5b44")
login_message.place(relx=0.5, rely=0.16, anchor="center")


#Label for the user to enter their username
user_name = ctk.CTkEntry(root, 
                         font=("Arial", 13), 
                         width=300, 
                         placeholder_text="Username", 
                         text_color="#7c5b44", 
                         fg_color="#fffef8")
user_name.place(relx=0.4, rely=0.25)

#Label for the user to enter their password.
user_password = ctk.CTkEntry(root, 
                             font=("Arial", 13), 
                             show="•", 
                             width=300, 
                             placeholder_text="Password", 
                             text_color="#7c5b44", 
                             fg_color="#fffef8")
user_password.place(relx=0.4, rely=0.33)

#Making a submit button for the login page, saving it to a text file.
submit_info = ctk.CTkButton(root, 
                            text="LOGIN", 
                            command=enter_user_name, 
                            fg_color="#7c5b44", 
                            text_color="#fffef8", 
                            hover_color="#b59a90",
                            width=300)
submit_info.place(relx=0.4, rely=0.4)

#Creating a button where the user can register and make a new account.

signup_text = ctk.CTkLabel(root, text="Don't have an account? Sign up here", text_color="#7c5b44", cursor="hand2", font=("Arial", 12, "underline"))
signup_text.place(relx=0.44, rely=0.45)
signup_text.bind("<Button-1>", lambda e: createnew_popup())

initialize_user_database()

root.mainloop()