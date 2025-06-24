'''This will be used as the homepage.
All functions coded will be put here (GUI and backend Python)'''

from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog

#------------ [STORAGE] ------------
'''Here is where the data from the "save new diary" will be saved'''
diaries = []  #Stores newly made diaries as dictionaries.
sidebar_buttons = []  #Stores as sidebar buttons.
current_diary_frame = None



#Define root.
root = tk.Tk()
root.title("Trial for Homepage")
root.geometry("1400x900")
root.configure(bg="#fffef8")  #Making background color.

def add_diary():


    '''Creating this function
    as a way to create the frame that when the
    button for adding a new diary is clicked, this
    frame will pop up'''

    def submit_diary():
        '''Def to save the diary in the dictionary, then
        alllowing the '''

        title = title_entry.get().strip()
        description = description_entry.get().strip()

        if not title:
            return  # Optionally add warning for empty title

        # Save diary data
        diary_data = {
            "title": title,
            "description": description,
            "image": image_path
        }
        diaries.append(diary_data)
        update_sidebar()
        new_window.destroy()

    def select_image():
        file_path = filedialog.askopenfilename(
            title="Select Cover Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")]
        )
        if file_path:
            image_path_var.set(file_path)

    new_window = Toplevel(root)
    new_window.title("New Diary Entry")
    new_window.geometry("600x600")
    new_window.configure(bg="#fffef8")

    #Adding the title
    title_label = Label(new_window, text="Diary Title:", font=("Verdana", 14), bg="#fffef8", fg="#9d7757")
    title_label.place(relx=0.04, rely=0.1)

    title_entry = Entry(new_window, font=("Verdana", 14), width=40, bd=2)
    title_entry.place(relx=0.2, rely=0.1)

    #Adding the description box.
    description_label = Label(new_window, text="Diary Description:", font=("Verdana", 14), bg="#fffef8", fg="#9d7757")
    description_label.place(relx=0.04, rely=0.2)

    description_entry = Text(new_window, font=("Verdana", 14), width=34, bd=2, wrap="word")
    description_entry.place(relx=0.28, rely=0.2, relheight=0.23)

    #Adding cover image for the diary.
    image_path_var = tk.StringVar()

    image_button = Button(new_window, text="Select Cover Photo", command=select_image, bg="#fffef8", fg="#9d7757", font=("Verdana", 14))
    image_button.place(relx=0.3, rely=0.55)

    submit_button = Button(new_window, text="Add Diary", command=submit_diary, bg="palegreen", font=("Verdana", 12))
    submit_button.place(relx=0.42, rely=0.65)

def update_sidebar():
    '''This function will be used to update the sidebar
    by adding the new diary names to the side bar.'''

    for btn in sidebar_buttons:
        btn.destroy()
    sidebar_buttons.clear()

    for idx, diary in enumerate(diaries):
        btn = Button(root, text=diary["title"], font=("Verdana", 10), bg="#d8cab6", width=20,
                     command=lambda i=idx: open_diary(i))
        btn.place(relx=0.01, rely=0.2 + 0.05 * idx)
        sidebar_buttons.append(btn)



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
    my_diaries_label = Label(main_frame, text="My Diaries", font=("Verdana", 56), bg="#fffef8", fg="#9d7757")
    my_diaries_label.place(relx=0.08, rely=0.12)

    #Creating the main frame in which the user can add a new diary.
    add_new_diary_frame = Frame(main_frame, bg="mediumpurple", highlightthickness=2, highlightcolor="#a89885")
    add_new_diary_frame.place(relx=0.4, rely=0.35, relheight=0.54, relwidth=0.24)

    #Creating a button for creating a new diary.
    add_diary_button = Button(add_new_diary_frame, text="+", font=("Arial", 40), bg="#f4c430", command=add_diary, bd=2)
    add_diary_button.place(relx=0.4, rely=0.43)

#Creating the main command for clicking the button

#Run the main functions.
sidebar()
topbar()
mainframe()

#Run the main root, after the functions.
root.mainloop()
