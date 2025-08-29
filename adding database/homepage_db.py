'''This version is the version in which I will be using custom
tkinter. In this one, I change from my regular tkinter to custom tkinter
to ensure the code looks neat and nice.'''

import customtkinter as ctk
import sqlite3
from tkinter import filedialog
from PIL import Image, ImageTk

db_file = "diaries.db"

def initialize_db():
    """Create database and table if not exists"""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS diaries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        description TEXT,
                        image TEXT
                      )''')
    conn.commit()
    conn.close()

def insert_diary(title, description, image):
    """Insert new diary entry"""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO diaries (title, description, image) VALUES (?, ?, ?)",
                   (title, description, image))
    conn.commit()
    conn.close()

def get_all_diaries():
    """Fetch all diaries"""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, image FROM diaries")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_diary_by_id(diary_id):
    """Fetch a single diary by ID"""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, image FROM diaries WHERE id = ?", (diary_id,))
    row = cursor.fetchone()
    conn.close()
    return row

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

    new_window = ctk.CTkToplevel(root)
    new_window.title("New Diary Entry")
    new_window.geometry("600x600")
    new_window.configure(fg_color="#fffef8")

    title_label = ctk.CTkLabel(new_window, text="Diary Title:", 
                               font=('Verdana', 18), 
                               fg_color="#fffef8", 
                               text_color="#7c5b44")
    title_label.place(relx=0.04, rely=0.1)

    #Adding a title.
    title_entry = ctk.CTkEntry(new_window, font=("Verdana", 14), 
                               text_color="#7c5b44", fg_color="#fffef8",
                               width=300, border_width=2)
    title_entry.place(relx=0.23, rely=0.1)

    description_label = ctk.CTkLabel(new_window, text="Description:", 
                                     font=('Verdana', 18), 
                                     fg_color="#fffef8", 
                                     text_color="#7c5b44")
    description_label.place(relx=0.04, rely=0.2)

    #Adding a diary description.
    description_entry = ctk.CTkTextbox(new_window, 
                                       font=('Verdana', 14), 
                                     text_color="#7c5b44", fg_color="#fffef8",
                                       width=340,border_width =2, wrap="word")
    description_entry.place(relx=0.23, rely=0.2, relheight=0.23)

    image_path_var = ctk.CTkStringVar()

    #Adding the cover image.
    image_button = ctk.CTkButton(new_window, text="Select Cover Image", command=select_image, fg_color="#f4c430", font=("Verdana", 12))
    image_button.place(relx=0.3, rely=0.55)

    submit_button = ctk.CTkButton(new_window, text="Add Diary", command=submit_diary, fg_color="palegreen", font=("Verdana", 12))
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
        btn = ctk.CTkButton(root, text=diary["title"], font=("Verdana", 10), fg_color="#d8cab6", width=20,
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

    current_diary_frame = ctk.CTkFrame(root, fg_color="#fffef8")
    current_diary_frame.place(relx=0.155, rely=0.156, relwidth=0.845, relheight=0.845)

    title_label = ctk.CTkLabel(current_diary_frame, text=diary["title"], font=("Verdana", 36), fg_color="#fffef8", text_color="#9d7757")
    title_label.pack(pady=40)

    if diary["image"]:
        try:
            img = Image.open(diary["image"])
            img = img.resize((300, 300), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)
            img_label = ctk.CTkLabel(current_diary_frame, image=img, fg_color="#fffef8")
            img_label.image = img
            img_label.pack()
        except:
            pass  #Image will not be shown if error occurs.

    description_label = ctk.CTkLabel(current_diary_frame, text=diary["description"], font=("Verdana", 14), fg_color="#fffef8", wraplength=800)
    description_label.pack(pady=20)


def sidebar():
    '''Code for the sidebar on the homepage'''
    side_bar = ctk.CTkFrame(root, fg_color="#e4d8c7")
    side_bar.place(relx=0, rely=0, relwidth=0.15, relheight=1)
    sidebar_separator = ctk.CTkFrame(root, fg_color="#a89885")
    sidebar_separator.place(relx=0.15, rely=0, relwidth=0.005, relheight=1)


def topbar():
    '''Code for the topbar on the homepage'''
    #Creating a main frame at the top of the homepage.
    top_bar = ctk.CTkFrame(root, fg_color="#fffef8")
    top_bar.place(relx=0.155, rely=0, relwidth=0.845, relheight=0.15)
    topbar_separator = ctk.CTkFrame(root, fg_color="#a89885") 
    topbar_separator.place(relx=0.15, 
                           rely=0.15, 
                           relwidth=1, 
                           relheight=0.006)

    try:
        image1 = "logo.png"
        image = Image.open(image1)
        image = image.resize((135, 135), Image.Resampling.LANCZOS)
        icon_image = ImageTk.PhotoImage(image)

        icon_label = ctk.CTkLabel(top_bar, image=icon_image)
        icon_label.image = icon_image
        icon_label.place(relx=0, rely=0, relwidth=0.1, relheight=1)
    except:
        pass  #Does not show if error occurs.


def mainframe():

    #Main frame.
    main_frame = ctk.CTkFrame(root, fg_color="#fffef8")
    main_frame.place(relx=0.155, rely=0.156, relwidth=0.845, relheight=0.845)

    my_diaries_label = ctk.CTkLabel(main_frame, 
                                    text="My Diaries", 
                                    font=("Helvetica", 56, "bold"), fg_color="#fffef8", 
                                    text_color="#9d7757")
    my_diaries_label.place(relx=0.08, rely=0.12)

    add_new_diary_frame = ctk.CTkFrame(main_frame, 
                                       fg_color="#fffef8", 
                                       border_width=2, border_color="#9d7757")
    add_new_diary_frame.place(relx=0.08, rely=0.35, relheight=0.54, relwidth=0.24)

    add_diary_button = ctk.CTkButton(add_new_diary_frame, text="+", 
                                     font=("Helvetica", 50), fg_color="#fffef8",
                                     text_color="#bed0d4", hover_color="#dae7e9",border_color="#a89885",
                                     command=add_diary, border_width=2, width=90,height=90)
    add_diary_button.place(relx=0.32, rely=0.38)

# -------- Main root window --------

root = ctk.CTk()
root.title("Diary App Homepage")
root.geometry("1400x900")
root.configure(fg_color="#fffef8")

#Running the main functions before running the root.mainloop()
sidebar()
topbar()
mainframe()

root.mainloop()

