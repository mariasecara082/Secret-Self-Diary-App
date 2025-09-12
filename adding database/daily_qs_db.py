'''this will be used as the questionnaire page.
all functions coded will be put here (GUI and back end python)'''

'''This version will be done using the database. This database
has been developed after changing the questionnaire page to ctk'''

import customtkinter as ctk
from tkinter import messagebox, IntVar
from PIL import Image, ImageTk
import subprocess
import sys
from tkinter import HORIZONTAL
from datetime import datetime
import sqlite3

# --- Get user_id from command line args ---
if len(sys.argv) > 1:
    user_id = sys.argv[1]  #Keep as string, convert to int IF needed.
    print(f"[DEBUG] Questionnaire received user_id={user_id}")
else:
    user_id = None
    print("[DEBUG] No user_id passed to questionnaire!")

#Initializing database:
def initialize_database():
    conn = sqlite3.connect("questionnaire.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_number INTEGER,
            response TEXT
        )
    """)
    conn.commit()
    conn.close() 

def save_response_to_db(question_number, response_text):

    '''This function will be used to saving the user's
    response to the database that was previously initialised.'''

    conn = sqlite3.connect("questionnaire.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO responses (question_number, response) VALUES (?, ?)", (question_number, response_text))
    conn.commit()
    conn.close()

#Creating the main root.
root = ctk.CTk()
root.title("Secret Self Diary App")
root.geometry("1400x900")
root.configure(fg_color="#fffef8")

#Creating a dictionary with the options in the questionnaire.
questionnaire_choices = [
    " Calm 😌"," Curious 👀"," Bored 🥱"," Annoyed 😑",
    " Stressed 😰"," Joyful 😄", " Grateful 🥹", " Lonely 😔", 
    " Ashamed 🙈", " Tired 😴", " Disappointed 🫠", " Peaceful ✌️"]

#Creating different frames for each question
frame_q1 = ctk.CTkFrame(root, fg_color="#fffef8")
frame_q2 = ctk.CTkFrame(root, fg_color="#fffef8")
frame_q3 = ctk.CTkFrame(root, fg_color="#fffef8")

#Packing the frames in the root.
for frame in (frame_q1, frame_q2, frame_q3):
    frame.place(relwidth=1, relheight=1)

#Switching between the frames.
def show_frame(frame):
    frame.tkraise()


#-------------- QUESTION 1 -------------- The GUI as well as the back ended code.
'''Here is the back ended code needed for
    creating the first question. Below, there is the selected_feelings,
    which is a list of all the options the user can choose. There is also
    a try and except to save the choices into a text file, and there is an if
    statement to warn the user that no option has been selected.'''

checkbox_vars = {}

welcome_message = ctk.CTkLabel(frame_q1, 
                            text="Welcome back, username", 
                            font=('Helvetica', 32), fg_color="#fffef8", text_color="#7c5b44")
welcome_message.place(relx=0.5, rely=0.15, anchor="center")

q1_label = ctk.CTkLabel(frame_q1, text="How are you feeling today?", font=("Helvetica", 23, "bold"), fg_color="#fffef8", text_color="#898686")
q1_label.place(relx=0.5, rely=0.25, anchor="center")

progressq1 = ctk.CTkProgressBar(frame_q1, width=400, progress_color="#bed0d4")
progressq1.place(relx=0.5, rely=0.05, anchor="center")
progressq1.set(0.33)

#Create checkboxes.
for idx, choice in enumerate(questionnaire_choices):
    var = IntVar()
    
    #Positioning in 3 rows and 3 columns.
    col = idx % 3
    row = idx // 3

    checkbox = ctk.CTkCheckBox(frame_q1,
    text=choice,
    variable=var,
    fg_color="#bed0d4",
    text_color="#333333", hover_color="#dae7e9",
    font=("Arial", 14)
)
    checkbox.place(relx=0.15 + col * 0.25, rely=0.4 + row * 0.08, relwidth=0.2, relheight=0.1)
    checkbox_vars[choice] = var

#Saving the answers into a database
def q1_answers():
    selected = [choice for choice, var in checkbox_vars.items() if var.get() == 1]
    if not selected:
        messagebox.showwarning("No selection", "Please select at least one feeling.")
        return
    try:
        save_response_to_db(1, ", ".join(selected))
        show_frame(frame_q2)
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong. Please try again!\n{e}")
        return
    if not selected:
        messagebox.showwarning("No selection", "Please select at least one option.")
        return
    print("User feelings submitted")

#Making the submit buttons for the questions
q1_submit_button = ctk.CTkButton(frame_q1, text="Next", 
                                 font=("Arial", 15), fg_color="#bed0d4", 
                                 command=q1_answers, text_color="#614836",
                                 hover_color="#dae7e9")
q1_submit_button.place(relx=0.75, rely=0.85, relwidth=0.1, relheight=0.05)


#-------------- QUESTION 2 -------------- The GUI as well as the back ended code.
'''This def will be used to create the GUI for
    the second question in the questionnaire. It opens right after
    the submit button to the question 1 is pressed. Unlike in the 
    past, instead of destroying the window and creating a new one,
    this will actually change the frames between each other.'''

ctk.CTkLabel(frame_q2, text="Welcome back, username", font=("Biski", 25), fg_color="#fffef8", text_color="#7c5b44").place(relx=0.5, rely=0.15, anchor="center")

progressq2 = ctk.CTkProgressBar(frame_q2, width=400, progress_color="#bed0d4")
progressq2.place(relx=0.5, rely=0.05, anchor="center")
progressq2.set(0.66)

ctk.CTkLabel(frame_q2, text="What was the highlight of your day?", font=("Helvetica", 23, "bold"), fg_color="#fffef8", text_color="#898686").place(relx=0.5, rely=0.22, anchor="center")

q2_entry = ctk.CTkEntry(frame_q2, width=400, font=("Arial", 14))
q2_entry.place(relx=0.5, rely=0.4, anchor="center")

def q2_answers():
    highlight = q2_entry.get().strip()
    if not highlight:
        messagebox.showwarning("Empty Field", "Please enter your highlight.")
        return
    try:
        save_response_to_db(2, highlight)
        show_frame(frame_q3)
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong. Please try again!\n{e}")
        return

ctk.CTkButton(frame_q2, text="Next", 
                                 font=("Arial", 15), fg_color="#bed0d4", 
                                 command=q2_answers, text_color="#614836",
                                 hover_color="#dae7e9").place(relx=0.75, rely=0.85, relwidth=0.1, relheight=0.05)

#-------------- QUESTION 3 -------------- The GUI as well as the back ended code.
ctk.CTkLabel(frame_q3, text="Welcome back, username", 
             font=("Biski", 25), 
             fg_color="#fffef8", 
             text_color="#7c5b44").place(relx=0.5, rely=0.15, anchor="center")

#Creating a progress bar 
progressq3 = ctk.CTkProgressBar(frame_q3, width=400, progress_color="#bed0d4")
progressq3.place(relx=0.5, rely=0.05, anchor="center")
progressq3.set(1)

ctk.CTkLabel(frame_q3, text="Rate your day on a scale from 1-10:", 
             font=("Helvetica", 23, "bold"), fg_color="#fffef8", 
             text_color="#898686").place(relx=0.5, rely=0.22, anchor="center")

q3_slider = ctk.CTkSlider(frame_q3, from_=0, to=10, number_of_steps=20, width=600)
q3_slider.set(5)
q3_slider.place(relx=0.5, rely=0.4, anchor="center")

def q3_answers():

    '''This function is being used to save the question 3
    answers into the database by calling the function
    named save_response_to_db'''
    rating = round(q3_slider.get())
    try:
        save_response_to_db(3, f"{rating}/10")
        root.destroy()

        homepage_path = "/Users/maria/Desktop/13DDT/13DDT-PROG-MariaSecara/Secret Self Diary App/adding database/homepage.py"
        if user_id:
            print(f"[DEBUG] Launching homepage with user_id={user_id}")
            subprocess.Popen([sys.executable, homepage_path, str(user_id)])
        else:
            print("[DEBUG] No user_id found, launching homepage without user")
            subprocess.Popen([sys.executable, homepage_path])

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong, please try again:\n{e}")

ctk.CTkButton(frame_q3, text="Submit", 
                                 font=("Arial", 15), fg_color="#bed0d4", 
                                 command=q3_answers, text_color="#614836",
                                 hover_color="#dae7e9").place(relx=0.75, rely=0.85, relwidth=0.1, relheight=0.05)
initialize_database()


show_frame(frame_q1)
root.mainloop()