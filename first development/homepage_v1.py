'''This will be used as the homepage.
All functions coded will be put here (GUI and backend Python)'''

from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk

#Define root.
root = tk.Tk()
root.title("Trial for Homepage")
root.geometry("1400x900")
root.configure(bg="#fffef8")  #Making background color.

def sidebar():

    '''The code for the GUI in the side bar on the side of the page.'''

    side_bar = Frame(root, bg="#e4d8c7")
    side_bar.place(relx=0, rely=0, relwidth=0.15, relheight=1)
    sidebar_separator = Frame(root, bg="#a89885")
    sidebar_separator.place(relx=0.15, rely=0, relwidth=0.005, relheight=1)

def topbar():

    '''The code for the GUI in the main bar at the top of the page.'''

    top_bar = Frame(root, bg="#fffef8")
    top_bar.place(relx=0.155, rely=0, relwidth=0.845, relheight=0.15)
    topbar_separator = Frame(root, bg="#a89885")
    topbar_separator.place(relx=0.15, rely=0.15, relwidth=1, relheight=0.006)

    #Moving image to top bar.
    image1 = "logo.png"  #Path to the logo.
    image = Image.open(image1)
    image = image.resize((135, 135), Image.Resampling.LANCZOS)
    icon_image = ImageTk.PhotoImage(image)

    icon_label = Label(top_bar, image=icon_image)
    icon_label.image = icon_image 
    icon_label.place(relx=0, rely=0, relwidth=0.1, relheight=1)

def mainframe():
    '''Main content area of the homepage.'''
    main_frame = Frame(root, bg="#fffef8")
    main_frame.place(relx=0.155, rely=0.156, relwidth=0.845, relheight=0.845)

    #Creating a main heading for the page.
    my_diaries_label = Label(main_frame, text="My Diaries", font=("Verdana", 56), bg="#fffef8")
    my_diaries_label.place(relx=0.08, rely=0.12)

    #Creating the main frame in which the user can add a new diary.
    add_new_diary_frame = Frame(main_frame, bg="mediumpurple", bd=2)
    add_new_diary_frame.place(relx=0.4, rely=0.35, relheight=0.54, relwidth=0.24)

    #Creating a button for creating a new diary.
    add_diary_button = Button(add_new_diary_frame, text="+", font=("Arial", 40), bg="#f4c430", command=add_diary)
    add_diary_button.place(relx=0.4, rely=0.43)

#Creating the main command for clicking the button

#Run the main functions.
sidebar()
topbar()
mainframe()

#Run the main root, after the functions.
root.mainloop()
