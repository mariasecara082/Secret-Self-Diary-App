'''this will be used as the questionnaire page.
all functions coded will be put here (GUI and back end python)'''
from tkinter import *
import webbrowser
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

print('massive change')

#Creating a dictionary with the options in the questionnaire.
questionnaire_questions = {
    "question":"How are you feeling today?",
    "choices":["Calm","Curious","Bored","Annoyed","Stressed","Joyful", "Gratefull", "Lonely", "Ashamed", "Tired", "Disappointed", "Peaceful"]
}

#Function where the users can submit their choices.
def q1_answers():

    '''Here is the back ended code needed for
    creating the first question. Below, there is the selected_feelings,
    which is a list of all the options the user can choose. There is also
    a try and except to save the choices into a text file, and there is an if
    statement to warn the user that no option has been selected.'''

    selected_feelings = [choice for choice, var in checkbox_vars.items() if var.get() == 1]
    
    try:
        with open("daily_questionnaire.txt", "a") as f:
            f.write(f"{selected_feelings}\n")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong. Please try again!\n{e}")
    if not selected_feelings:
        messagebox.showwarning("No selection", "Please select at least one option.")
        return
    print("User feelings submitted")
    root.destroy()
    q2_window_open()

def q2_answers():
    hilite_day = q2_entry.get().strip()

    try:
        with open("daily_questionnaire.txt", "a") as f:
            f.write(f"Highlight: {hilite_day}\n")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong. Please try again!\n{e}")
    if not hilite_day:
        messagebox.showerror("Error", f"Please enter a response and try again\n{e}")
        return
    print("Highlight of day submitted")
    q2_window.destroy()
    q3_window_open()


def q2_window_open():

    '''This def will be used to create the GUI for
    the second question in the questionnaire. It opens right after
    the root window (which belongs to question 1) 
    get destroyed.'''

    global q2_window, q2_entry
    q2_window = tk.Tk()
    q2_window.title("Secret Self Diary App")
    q2_window.geometry("1400x900")
    q2_window.configure(bg="#fffef8") #Making the root colour have a background colour.
    q2_window.iconbitmap("images/logo.ico")

    q2_label = tk.Label(q2_window, text="What was the highlight of your day?", font=("Arial", 16), bg="#fffef8")
    q2_label.pack(pady=30)

    q2_entry = Entry(q2_window, text="Write answer here", fg="grey", width=50, font=("Arial", 14))
    q2_entry.pack(pady=10)

    q2_submit_button = tk.Button(q2_window, text="Submit", font=("Arial", 14), bg="#f4c430", command=q2_answers)
    q2_submit_button.pack(pady=20)
    
    q2_window_open.mainloop()

def q3_answers():

    '''This def will be used to create the
    back ended things needed for the third question of the code.'''

    rating = q3_slider.get()
    try:
        with open("daily_questionnaire.txt", "a") as f:
            f.write(f"Day rating: {rating}/10\n")
        #Destroying and closing this window
        q3_window.destroy()
        script_path = "/Users/maria/Desktop/13DDT/13DDT-PROG-MariaSecara/Secret Self Diary App/second development/homepage_v2.py" 
        '''opening up the daily questionnaire'''
        subprocess.Popen([sys.executable, script_path])
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong, please try again:\n{e}")


def q3_window_open():

    '''This def will be used to create the GUI for
    the third question in the questionnaire. It opens right after
    the q2 window (which belongs to question 2) 
    get destroyed.'''

    global q3_window, q3_slider
    q3_window = tk.Tk()
    q3_window.title("Secret Self Diary App")
    q3_window.geometry("1400x900")
    q3_window.configure(bg="#fffef8") #Making the root colour have a background colour.
    q3_window.iconbitmap("images/logo.ico")

    q3_label = tk.Label(q3_window, text="Rate your day on a scale from 1-10:", font=("Arial", 16), bg="#fffef8")
    q3_label.pack(pady=30)

    q3_slider = tk.Scale(q3_window, from_=0, to=10, orient=HORIZONTAL, length=500, tickinterval=0.5, font=("Arial", 12))
    q3_slider.set(5)
    q3_slider.pack(pady=20)
    q3_submit_button = tk.Button(q3_window, text="Submit", font=("Arial", 14), bg="#f4c430", command=q3_answers)
    q3_submit_button.pack(pady=20)
    
    q3_window_open.mainloop()

#Creating the main window in which the quiz will be located.
root = tk.Tk()
root.title("Secret Self Diary App")
root.geometry("1400x900")
root.configure(bg="#fffef8") #Making the root colour have a background colour.
root.iconbitmap("images/logo.ico") #Adding the logo

q1_label = tk.Label(root, text=questionnaire_questions["question"], font=("Arial", 16), bg="#fffef8")
q1_label.pack(pady=30)

#Create checkboxes.
checkbox_vars = {}
for choice in questionnaire_questions["choices"]:
    var = IntVar()
    checkbox = tk.Checkbutton(root, text=choice, variable=var, font=("Arial", 13))
    checkbox.pack(padx=40, anchor="w")
    checkbox_vars[choice] = var

#Making the submit buttons for the questions
q1_submit_button = tk.Button(root, text="Submit", font=("Arial", 14), bg="#f4c430", command=q1_answers)
q1_submit_button.pack(pady=30)

root.mainloop()