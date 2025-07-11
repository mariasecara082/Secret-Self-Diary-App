'''this will be used as the questionnaire page.
all functions coded will be put here (GUI and back end python)'''

'''Version Three (V3, this version), is the version with changed GUI, as well
as changed transitioning between the questions inside the quenstionnaire.
Instead of using a new window to change between the questions, a new
frame will be made. The option to go back to the old  question to
give the users freedom to change their answers. The final answers will
only be seen on the textfile once the whole questionnaire has been submitted'''

from tkinter import *
import subprocess
import sys
import tkinter as tk
from tkinter import IntVar, messagebox
from PIL import Image, ImageTk
from tkinter import ttk

#Creating a dictionary with the options in the questionnaire.
questionnaire_choices = [
    " Calm 😌"," Curious 👀"," Bored 🥱"," Annoyed 😑",
    " Stressed 😰"," Joyful 😄", " Grateful 🥹", " Lonely 😔", 
    " Ashamed 🙈", " Tired 😴", " Disappointed 🫠", " Peaceful ✌️"]

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

    q2_label = tk.Label(q2_window, text="What was the highlight of your day?", font=("Arial", 25), bg="#fffef8", fg="#898686")
    q2_label.place(relx=0.5, rely=0.3, anchor="center")
    
    q2_entry = Entry(q2_window, fg="#898686", width=50, font=("Arial", 14))
    q2_entry.place(relx=0.5, rely=0.4, anchor="center")

    q2_submit_button = tk.Button(q2_window, text="Submit", font=("Arial", 14), bg="#f4c430", command=q2_answers)
    q2_submit_button.place(relx=0.75, rely=0.85, relwidth=0.1, relheight=0.05)
    
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
    q3_label.place(relx=0.5, rely=0.1, anchor="center")

    q3_slider = tk.Scale(q3_window, from_=0, to=10, orient=HORIZONTAL, length=500, tickinterval=0.5, font=("Arial", 12))
    q3_slider.set(5)
    q3_slider.pack(pady=20)
    q3_submit_button = tk.Button(q3_window, text="Submit", font=("Arial", 14), bg="#f4c430", command=q3_answers)
    q3_submit_button.place(relx=0.75, rely=0.85, relwidth=0.1, relheight=0.05)
    
    q3_window_open.mainloop()

#Creating the main window in which the quiz will be located.
root = tk.Tk()
root.title("Secret Self Diary App")
root.geometry("1400x900")
root.configure(bg="#fffef8") #Making the root colour have a background colour.
root.iconbitmap("images/logo.ico") #Adding the logo

#Making a frame to outline the questionnaire
#This will take away from the whitespace a bit
main_frame = Frame(root, bg="#ffffff")

#Images for the checked and unchecked checklist boxes
def flatten_transparent_png(image_path, bg_color="#fffef8"):
    im = Image.open(image_path).convert("RGBA")
    background = Image.new("RGBA", im.size, bg_color)
    alpha = im.split()[-1]
    background.paste(im, mask=alpha)
    return background.convert("RGB")

unchecked_pil = flatten_transparent_png("untickedbox.png").resize((48, 48), Image.Resampling.LANCZOS)
checked_pil = flatten_transparent_png("tickedbox.png").resize((48, 48), Image.Resampling.LANCZOS)

unchecked_image = ImageTk.PhotoImage(unchecked_pil)
checked_image = ImageTk.PhotoImage(checked_pil)


q1_label = tk.Label(root, text="How are you feeling today?", font=("Arial", 25), bg="#fffef8")
q1_label.place(relx=0.5, rely=0.2, anchor="center")

progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress.place(relx=0.5, rely=0.05, anchor="center")
progress["value"] = 33

#Create checkboxes.
checkbox_vars = {}
for idx, choice in enumerate(questionnaire_choices):
    var = IntVar()
    
    
    #Positioning in 3 rows and 3 columns.
    col = idx % 3
    row = idx // 3

    checkbox = tk.Checkbutton(#Images
    text=choice,
    variable=var,
    image=unchecked_image,
    selectimage=checked_image,
    compound="left", #Moves the image to the left of the text
    indicatoron=False,  #Removes small default box
    bg="#fffef8", fg="#fffef8"
    )
    checkbox.place(relx=0.15 + col * 0.25, rely=0.4 + row * 0.08, relwidth=0.1, relheight=0.06)
    checkbox_vars[choice] = var
    
    checkbox.image = unchecked_image 
    checkbox.selectimage = checked_image

#Making the submit buttons for the questions
q1_submit_button = tk.Button(root, text="Next", font=("Arial", 15), bg="mediumpurple", command=q1_answers)
q1_submit_button.place(relx=0.75, rely=0.85, relwidth=0.1, relheight=0.05)

root.mainloop()