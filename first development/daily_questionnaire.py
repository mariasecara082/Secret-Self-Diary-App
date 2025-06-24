'''this will be used as the questionnaire page.
all functions coded will be put here (GUI and back end python)'''
from tkinter import *
import webbrowser
import tkinter as tk
from tkinter import messagebox

#Creating a dictionary with the options in the questionnaire.
questionnaire_questions = {
    "question":"How are you feeling today?",
    "choices":["Calm","Curious","Bored","Annoyed","Stressed","Joyful", "Gratefull", "Lonely", "Ashamed", "Tired", "Disappointed", "Peaceful"]
}

#Function where the users can submit their choices.
def q1_answers():
    selected_feelings = [choice for choice, var in checkbox_vars.items() if var.get() == 1]
    
    try:
        with open("daily_questionnaire.txt", "a") as f:
            f.write(f"{selected_feelings}\n")
        root.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong. Please try again!\n{e}")
    if not selected_feelings:
        messagebox.showwarning("No selection", "Please select at least one option.")
        return
    print("User feelings submitted")


def q2_answers():
    global q2_window, q2_entry
    hilite_day = q2_entry.get().strip()

    try:
        with open("daily_questionnaire.txt", "a") as f:
            f.write(f"{hilite_day}\n")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong. Please try again!\n{e}")
    if not hilite_day:
        messagebox.showerror("Error", f"Please enter a response and try again\n{e}")
        return
    print("Highlight of day submitted")

#Creating the main window in which the quiz will be located.
root = tk.Tk()
root.title("Secret Self Diary App")
root.geometry("700x1200")
root.configure(bg="#fffef8") #Making the root colour have a background colour.

#Second question window
q2_window = Toplevel()
q2_window.title("Secret Self Diary App")
q2_window.geometry("700x1200")
q2_window.configure(bg="#fffef8") #Making the root colour have a background colour.

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

q2_submit_button = tk.Button(q2_window, text="Submit", font=("Arial", 14), bg="#f4c430", command=q2_answers )

root.mainloop()