'''this will be used as the login page.
all functions coded will be put here (GUI and back end python)'''
from tkinter import *
import webbrowser
import tkinter as tk
from tkinter import messagebox

#Here, I am starting to code the GUI for the login page. For the sake of this testing, use the username test and test123.
def enter_user_name():
    username = user_name.get().strip()
    password = user_password.get().strip()

    # Check for empty fields.
    if not username or not password:
        messagebox.showwarning("Validation Error", "Username and password cannot be empty.")
        return

    #Checking password validity.
    special_chars = "!@#$%^&*()}~`,.<>?/:;{[]|\+=™¡£¢∞§¶•ªºåœ∑´®†¥¨ˆøπåß∂ƒ©˙∆˚¬≈ç√∫˜µ≤≥"
    if len(password) < 8:
        messagebox.showwarning("Validation Error", "Password must be at least 8 characters.")
        return
    if len(password) > 20:
        messagebox.showwarning("Validation Error", "Password cannot be more than 20 characters.")
        return
    if not any(char in special_chars for char in password):
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
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong, please try again:\n{e}")


#Creating a main window using root = tk.Tk().
root = tk.Tk()
root.title("Secret Self Diary App")
root.geometry("700x1200")
root.configure(bg="#fffef8") #Making the root colour have a background colour.


welcome_message = tk.Label(root, text="*:･ﾟ✧*:･ﾟ Welcome to Secret Self Diary App *:･ﾟ✧*:･ﾟ", font=('Helvetica', 26), bg="mediumpurple")
welcome_message.pack(pady=40)


#Label for the user to enter their username
name = Label(root, text="Username", font=("Arial", 13), bg="mediumpurple").pack(pady=30)
user_name = Entry(root, font=("Arial", 11), width=35)
user_name.pack(pady=(60))

#Label for the user to enter their password.
password = Label(root, text="Password", font=("Arial", 13), bg="mediumpurple").pack(pady=(20,3))
user_password = Entry(root, font=("Arial", 11), show="•", width=35)
user_password.pack(pady=20)

#Making a submit button for the login page, saving it to a text file.
submit_info = Button(root, text="Log In", font=("arial", 15), command=enter_user_name, bg="red", fg="mediumPurple").place(x=400,y=250)


root.mainloop()

#create_gui()