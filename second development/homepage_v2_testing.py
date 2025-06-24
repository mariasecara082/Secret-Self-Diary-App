from tkinter import *
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Diary App Homepage")
root.geometry("1400x900")
root.configure(bg="#fffef8")

 #Creating the main frame in which the user can add a new diary.
add_new_diary_frame = Frame(root, bg="#f4c430", highlightbackground="hotpink", # Border color
    highlightthickness=4)
add_new_diary_frame.place(relx=0.4, rely=0.35, relheight=0.54, relwidth=0.24)

#Creating a button for creating a new diary.
add_diary_button = Button(add_new_diary_frame, text="+", font=("Arial", 40), bg="#f4c430", bd=2, highlightbackground="#a89885")
add_diary_button.place(relx=0.4, rely=0.43)

root.mainloop()
