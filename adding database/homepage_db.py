from tkinter import *
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

#Storage.
'''Here is where the data from the "save new diary" will be saved'''
diaries = []  #Diaries get stored as a dictionary
sidebar_buttons = []  #Buttons that link to new diaries
current_diary_frame = None  #Shows which diary is currently open

#Functions.

def add_diary():
    '''Creating this function
    as a way to create the frame that when the
    button for adding a new diary is clicked, this
    frame will pop up''' 

    def submit_diary():
        '''Def to save the diary in the dictionary, then
        allowing the user to access it through the
        sidebar.'''
        title = title_entry.get()
        description = description_entry.get("1.0", "end-1c")
        image_path = image_path_var.get()

        if not title:
            return  #Add warning for empty title

        #Saves diary data.
        diary_data = {
            "title": title,
            "description": description,
            "image": image_path
        }
        diaries.append(diary_data)
        update_sidebar()
        new_window.destroy()

    def select_image():
        '''Allowing the users to insert an image
        from their computer using filedialog. This selected
        image will be used as the cover image for the specific
        made diary'''
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

    title_label = Label(new_window, text="Diary Title:", font=("Verdana", 14), bg="#fffef8", fg="#9d7757")
    title_label.place(relx=0.04, rely=0.1)

    #Adding a title.
    title_entry = Entry(new_window, font=("Verdana", 14), width=40, bd=2)
    title_entry.place(relx=0.2, rely=0.1)

    description_label = Label(new_window, text="Diary Description:", font=("Verdana", 14), bg="#fffef8", fg="#9d7757")
    description_label.place(relx=0.04, rely=0.2)

    #Adding a diary description.
    description_entry = Text(new_window, font=("Verdana", 14), width=34, bd=2, wrap="word")
    description_entry.place(relx=0.28, rely=0.2, relheight=0.23)

    image_path_var = tk.StringVar()

    #Adding the cover image.
    image_button = Button(new_window, text="Select Cover Image", command=select_image, bg="#f4c430", font=("Verdana", 12))
    image_button.place(relx=0.3, rely=0.55)

    submit_button = Button(new_window, text="Add Diary", command=submit_diary, bg="palegreen", font=("Verdana", 12))
    submit_button.place(relx=0.42, rely=0.65)


def update_sidebar():
    '''Adding the newly created diary to the 
    sidebar as a button. The user will then be able to access it by the function
    open_diary, and then the user will have the ability to create new diary entries'''

    #Remove existing buttons in the sidebar.
    for btn in sidebar_buttons:
        btn.destroy()
    sidebar_buttons.clear()

    for idx, diary in enumerate(diaries): #Loops through each diary on the diaries list.
        btn = Button(root, text=diary["title"], font=("Verdana", 10), bg="#d8cab6", width=20,
                     command=lambda i=idx: open_diary(i)) #i=idx needs to prevent the buttons from opening last diary.
        btn.place(relx=0.01, rely=0.2 + 0.05 * idx)
        sidebar_buttons.append(btn)


def open_diary(index):
    '''Def that will open the diary once clicked through the 
    side bar. This means that once the diary is created and
    placed in the side bar, the user is able to click it,
    opening a new page without actually creating a toplevel window on top'''
    global current_diary_frame
    diary = diaries[index]

    if current_diary_frame:
        current_diary_frame.destroy()

    current_diary_frame = Frame(root, bg="#fffef8")
    current_diary_frame.place(relx=0.155, rely=0.156, relwidth=0.845, relheight=0.845)

    title_label = Label(current_diary_frame, text=diary["title"], font=("Verdana", 36), bg="#fffef8", fg="#9d7757")
    title_label.pack(pady=40)

    if diary["image"]:
        try:
            img = Image.open(diary["image"])
            img = img.resize((300, 300), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)
            img_label = Label(current_diary_frame, image=img, bg="#fffef8")
            img_label.image = img
            img_label.pack()
        except:
            pass  #Image will not be shown if error occurs.

    description_label = Label(current_diary_frame, text=diary["description"], font=("Verdana", 14), bg="#fffef8", wraplength=800)
    description_label.pack(pady=20)


def sidebar():
    '''Code for the sidebar on the homepage'''
    side_bar = Frame(root, bg="#e4d8c7")
    side_bar.place(relx=0, rely=0, relwidth=0.15, relheight=1)
    sidebar_separator = Frame(root, bg="#a89885")
    sidebar_separator.place(relx=0.15, rely=0, relwidth=0.005, relheight=1)


def topbar():
    '''Code for the topbar on the homepage'''
    top_bar = Frame(root, bg="#fffef8")
    top_bar.place(relx=0.155, rely=0, relwidth=0.845, relheight=0.15)
    topbar_separator = Frame(root, bg="#a89885")
    topbar_separator.place(relx=0.15, rely=0.15, relwidth=1, relheight=0.006)

    try:
        image1 = "logo.png"
        image = Image.open(image1)
        image = image.resize((135, 135), Image.Resampling.LANCZOS)
        icon_image = ImageTk.PhotoImage(image)

        icon_label = Label(top_bar, image=icon_image)
        icon_label.image = icon_image
        icon_label.place(relx=0, rely=0, relwidth=0.1, relheight=1)
    except:
        pass  #Does not show if error occurs.


def mainframe():

    #Main frame.
    main_frame = Frame(root, bg="#fffef8")
    main_frame.place(relx=0.155, rely=0.156, relwidth=0.845, relheight=0.845)

    my_diaries_label = Label(main_frame, text="My Diaries", font=("Verdana", 56), bg="#fffef8", fg="#9d7757")
    my_diaries_label.place(relx=0.08, rely=0.12)

    add_new_diary_frame = Frame(main_frame, bg="#fffef8", bd=2, highlightbackground="hotpink",
    highlightthickness=7)
    add_new_diary_frame.place(relx=0.4, rely=0.35, relheight=0.54, relwidth=0.24)

    add_diary_button = Button(add_new_diary_frame, text="+", font=("Arial", 40), bg="#f4c430", command=add_diary, bd=2)
    add_diary_button.place(relx=0.4, rely=0.43)

# -------- Main root window --------

root = tk.Tk()
root.title("Diary App Homepage")
root.geometry("1400x900")
root.configure(bg="#fffef8")

#Running the main functions before running the root.mainloop()
sidebar()
topbar()
mainframe()

root.mainloop()