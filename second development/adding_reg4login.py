'''this will be used as the login page.
all functions coded will be put here (GUI and back end python)'''
from tkinter import *
import webbrowser
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

#Here, I am starting to code the GUI for the login page. For the sake of this testing, use the username test and test123.
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

    #Check for allowed usernames. - will have to change when users are getting made.
    allowed_users = {"maria": "mariasecara1!","test":"test123@"}
    if username not in allowed_users or allowed_users[username] != password:
        messagebox.showerror("Login Failed", "Invalid username or password.")
        return

    # If all checks pass, save the login info
    try:
        with open("login_info_file.txt", "a") as f:
            f.write(f"{username}, {password}\n")
        messagebox.showinfo("Success", "Thank you for logging in :).")
        #Destroying and closing this window
        root.destroy()
        script_path = "/Users/maria/Desktop/13DDT/13DDT-PROG-MariaSecara/Secret Self Diary App/daily_qs_ver2.py" 
        '''opening up the daily questionnaire'''
        subprocess.Popen([sys.executable, script_path])
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong, please try again:\n{e}")

def createnew_popup():

    '''this creates a new pop-up window when the button
    to register a new user is pressed. the window
    has certain dimensions, just like the root'''

    popupwindow = Toplevel(root)
    popupwindow.title("Register new user")
    popupwindow.geometry("500x300")
    popupwindow.configure(bg="#fffef8")
    popupwindow.iconbitmap("images/logo.ico")

    Label(popupwindow, text="Create username:", font=("Arial", 13), bg="mediumpurple").pack(pady=5)
    register_username_entry = Entry(popupwindow)
    register_username_entry.pack(pady=5)

    Label(popupwindow, text="Create password: (8-20 characters long)", font=("Arial", 13), bg="mediumpurple").pack(pady=5)
    register_password_entry = Entry(popupwindow, show="•")
    register_password_entry.pack(pady=5)

    def save_new_user(): 

        '''this function is made to save 
        the new registered user into a textfile'''

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
        
        #Saving the new registrated user into a text file:

        try:
            with open("registered_users.txt", "a") as file:
                file.write(f"{reg_username}, {reg_password}\n")
            messagebox.showinfo("Success", "User registered successfully!")
            popupwindow.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save user:\n{e}")

    Button(popupwindow, text="Create New User", command=save_new_user, bg="red", fg="mediumPurple").pack(pady=20)

    
    #new_user = new_user_name.get().strip()


#Creating a main window using root = tk.Tk().
root = tk.Tk()
root.title("Secret Self Diary App")
root.geometry("1400x900")
root.configure(bg="#fffef8") #Making the root colour have a background colour.
root.iconbitmap("images/logo.ico")

#Welcome message displayed at the top of the root.
welcome_message = tk.Label(root, text="*:･ﾟ✧*:･ﾟ Welcome to Secret Self Diary App *:･ﾟ✧*:･ﾟ", font=('Helvetica', 26), bg="mediumpurple")
welcome_message.pack(pady=(20,0))


#Label for the user to enter their username
name = Label(root, text="Username", font=("Arial", 13), bg="mediumpurple").pack(pady=(20,1))
user_name = Entry(root, font=("Arial", 11), width=35)
user_name.pack(pady=(20,2))

#Label for the user to enter their password.
password = Label(root, text="Password (8-20 characters long)", font=("Arial", 13), bg="mediumpurple").pack(pady=(20,3))
user_password = Entry(root, font=("Arial", 11), show="•", width=35)
user_password.pack(pady=(20,2))

#Making a submit button for the login page, saving it to a text file.
submit_info = Button(root, text="Log In", font=("arial", 15), command=enter_user_name, bg="red", fg="mediumPurple").place(x=400,y=250)

#Creating a button where the user can register and make a new account.

register_user = Button(root, text="Register new user:", font=("arial", 15), command=createnew_popup, bg="mediumPurple", fg="mediumPurple").place(x=180,y=250)


root.mainloop()

#create_gui()