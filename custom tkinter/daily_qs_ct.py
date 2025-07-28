'''this will be used as the questionnaire page.
all functions coded will be put here (GUI and back end python)'''

'''Custom Tkinter Version, is the version with changed and developed GUI.
The final answers will only be seen on the textfile once the 
whole questionnaire has been submitted'''

import customtkinter as ctk
from tkinter import messagebox, IntVar
from PIL import Image, ImageTk
import subprocess
import sys
from tkinter import HORIZONTAL
from datetime import datetime

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

#-------------- Question 1 -------------- The GUI as well as the back ended code.
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
    fg_color="#f4c430",
    text_color="#333333",
    font=("Arial", 14)
)
    checkbox.place(relx=0.15 + col * 0.25, rely=0.4 + row * 0.08, relwidth=0.2, relheight=0.1)
    checkbox_vars[choice] = var

#Saving the answers into a textfile
def q1_answers():
    selected = [choice for choice, var in checkbox_vars.items() if var.get() == 1]
    if not selected:
        messagebox.showwarning("No selection", "Please select at least one feeling.")
        return
    try:
        with open("daily_questionnaire.txt", "a") as f:
            f.write(f"Feelings: {selected}\n")
        show_frame(frame_q2)
    except Exception as e:
        messagebox.showerror("Error", str(e))

#Making the submit buttons for the questions
q1_submit_button = ctk.CTkButton(frame_q1, text="Next", font=("Arial", 15), fg_color="mediumpurple", command=q1_answers)
q1_submit_button.place(relx=0.75, rely=0.85, relwidth=0.1, relheight=0.05)

#-------------- Question 2 -------------- The GUI as well as the back ended code.
'''This def will be used to create the GUI for
    the second question in the questionnaire. It opens right after
    the submit button to the question 1 is pressed. Unlike in the 
    past, instead of destroying the window and creating a new one,
    this will actually change the frames between each other.'''

ctk.CTkLabel(frame_q2, text="Welcome back, username", font=("Biski", 25), fg_color="#fffef8", text_color="#7c5b44").place(relx=0.5, rely=0.15, anchor="center")

progressq2 = ctk.CTkProgressBar(frame_q2, width=400)
progressq2.place(relx=0.5, rely=0.05, anchor="center")
progressq2.set(0.66)

ctk.CTkLabel(frame_q2, text="What was the highlight of your day?", font=("Arial", 20), fg_color="#fffef8", text_color="#898686").place(relx=0.5, rely=0.22, anchor="center")

q2_entry = ctk.CTkEntry(frame_q2, width=400, font=("Arial", 14))
q2_entry.place(relx=0.5, rely=0.4, anchor="center")

def q2_answers():
    highlight = q2_entry.get().strip()
    if not highlight:
        messagebox.showwarning("Empty Field", "Please enter your highlight.")
        return
    try:
        with open("daily_questionnaire.txt", "a") as f:
            f.write(f"Highlight: {highlight}\n")
        show_frame(frame_q3)
    except Exception as e:
        messagebox.showerror("Error", str(e))

ctk.CTkButton(frame_q2, 
                  text="Submit", 
                  font=("Arial", 14), 
                  fg_color="#f4c430", 
                  command=q2_answers).place(relx=0.75, rely=0.85, relwidth=0.1, relheight=0.05)

#-------------- Question 3 -------------- The GUI as well as the back ended code.
ctk.CTkLabel(frame_q3, text="Welcome back, username", font=("Biski", 25), fg_color="#fffef8", text_color="#7c5b44").place(relx=0.5, rely=0.15, anchor="center")

progressq3 = ctk.CTkProgressBar(frame_q3, width=400)
progressq3.place(relx=0.5, rely=0.05, anchor="center")
progressq3.set(1)

ctk.CTkLabel(frame_q3, text="Rate your day on a scale from 1-10:", font=("Arial", 20), fg_color="#fffef8", text_color="#898686").place(relx=0.5, rely=0.22, anchor="center")

q3_slider = ctk.CTkSlider(frame_q3, from_=0, to=10, number_of_steps=20)
q3_slider.set(5)
q3_slider.place(relx=0.32, rely=0.4)

def q3_answers():
    rating = round(q3_slider.get())
    try:
        with open("daily_questionnaire.txt", "a") as f:
            f.write(f"Day rating: {rating}/10\n")
            f.write(f"Submitted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        messagebox.showinfo("Submitted", "Your answers have been saved. Thank you!")
        root.destroy()
    except Exception as e:
        messagebox.showerror("Error", str(e))

ctk.CTkButton(frame_q3, text="Submit", font=("Arial", 14), fg_color="#f4c430", command=q3_answers).place(relx=0.75, rely=0.85, relwidth=0.1, relheight=0.05)


show_frame(frame_q1)
root.mainloop()