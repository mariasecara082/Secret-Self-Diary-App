'''This version is the version in which I will be adding a database to the 
homepagae. This makes saving files and newly made 
"diary" folders easier. '''

import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import sqlite3
import os

#-------------- DATABASE --------------
db_file = "diaries.db"

def init_db():

    '''Create database and table if not exists'''

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

    '''Insert new diary entry'''

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO diaries (title, description, image) VALUES (?, ?, ?)",
                   (title, description, image))
    conn.commit()
    conn.close()

def get_all_diaries():

    '''Get all diaries'''

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, image FROM diaries")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_diary_by_id(diary_id):

    '''Get a single diary by ID'''

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, image FROM diaries WHERE id = ?", (diary_id,))
    row = cursor.fetchone()
    conn.close()
    return row

# ---------------- GUI SETUP ----------------
sidebar_buttons = []
current_diary_frame = None

def add_diary():

    '''Create a new diary entry window'''

    def submit_diary():
        title = title_entry.get()
        description = description_entry.get("1.0", "end-1c")
        image_path = image_path_var.get()

        if not title:
            return  #Warning for empty title.

        #Save to database.
        insert_diary(title, description, image_path)
        update_sidebar()
        new_window.destroy()

    def select_image():
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

    title_entry = ctk.CTkEntry(new_window, font=("Verdana", 14),
                               text_color="#7c5b44", fg_color="#fffef8",
                               width=300, border_width=2)
    title_entry.place(relx=0.23, rely=0.1)

    description_label = ctk.CTkLabel(new_window, text="Description:",
                                     font=('Verdana', 18),
                                     fg_color="#fffef8",
                                     text_color="#7c5b44")
    description_label.place(relx=0.04, rely=0.2)

    description_entry = ctk.CTkTextbox(new_window,
                                       font=('Verdana', 14),
                                       text_color="#7c5b44", fg_color="#fffef8",
                                       width=340, border_width=2, wrap="word")
    description_entry.place(relx=0.23, rely=0.2, relheight=0.23)

    image_path_var = ctk.StringVar()

    image_button = ctk.CTkButton(new_window, text="Select Cover Image", command=select_image,
                                 fg_color="#f4c430", font=("Verdana", 12))
    image_button.place(relx=0.3, rely=0.55)

    submit_button = ctk.CTkButton(new_window, text="Add Diary", command=submit_diary,
                                  fg_color="palegreen", font=("Verdana", 12))
    submit_button.place(relx=0.42, rely=0.65)

def update_sidebar():

    '''Refresh sidebar with diaries from DB'''

    for btn in sidebar_buttons:
        btn.destroy()
    sidebar_buttons.clear()

    diaries = get_all_diaries()
    for idx, diary in enumerate(diaries):
        diary_id, title, _, _ = diary
        btn = ctk.CTkButton(root, text=title, font=("Verdana", 10),
                            fg_color="#d8cab6", width=20,
                            command=lambda i=diary_id: open_diary(i))
        btn.place(relx=0.01, rely=0.2 + 0.05 * idx)
        sidebar_buttons.append(btn)

def open_diary(diary_id):

    '''Open a diary by ID'''

    global current_diary_frame
    diary = get_diary_by_id(diary_id)
    if not diary:
        return

    _, title, description, image_path = diary

    if current_diary_frame:
        current_diary_frame.destroy()

    current_diary_frame = ctk.CTkFrame(root, fg_color="#fffef8")
    current_diary_frame.place(relx=0.155, rely=0.156, relwidth=0.845, relheight=0.845)

    title_label = ctk.CTkLabel(current_diary_frame, text=title, font=("Verdana", 36),
                               fg_color="#fffef8", text_color="#9d7757")
    title_label.pack(pady=40)

    if image_path:
        try:
            img = Image.open(image_path)
            img = img.resize((300, 300), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)
            img_label = ctk.CTkLabel(current_diary_frame, image=img, fg_color="#fffef8")
            img_label.image = img
            img_label.pack()
        except:
            pass

    description_label = ctk.CTkLabel(current_diary_frame, text=description,
                                     font=("Verdana", 14), fg_color="#fffef8", wraplength=800)
    description_label.pack(pady=20)

def sidebar():

    '''Making a side bar menu'''

    side_bar = ctk.CTkFrame(root, fg_color="#e4d8c7")
    side_bar.place(relx=0, rely=0, relwidth=0.15, relheight=1)
    sidebar_separator = ctk.CTkFrame(root, fg_color="#a89885")
    sidebar_separator.place(relx=0.15, rely=0, relwidth=0.005, relheight=1)

def topbar():

    '''Making a top bar menu'''

    top_bar = ctk.CTkFrame(root, fg_color="#fffef8")
    top_bar.place(relx=0.155, rely=0, relwidth=0.845, relheight=0.15)
    topbar_separator = ctk.CTkFrame(root, fg_color="#a89885")
    topbar_separator.place(relx=0.15, rely=0.15, relwidth=1, relheight=0.006)

    try:
        image1 = "logo.png"
        image = Image.open(image1)
        image = image.resize((135, 135), Image.Resampling.LANCZOS)
        icon_image = ImageTk.PhotoImage(image)

        icon_label = ctk.CTkLabel(top_bar, image=icon_image)
        icon_label.image = icon_image
        icon_label.place(relx=0, rely=0, relwidth=0.1, relheight=1)
    except:
        pass

def mainframe():

    '''Main frame in the root'''

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
                                     text_color="#bed0d4", hover_color="#dae7e9", border_color="#a89885",
                                     command=add_diary, border_width=2, width=90, height=90)
    add_diary_button.place(relx=0.32, rely=0.38)

#Main root window.
init_db()

root = ctk.CTk()
root.title("Diary App Homepage")
root.geometry("1400x900")
root.configure(fg_color="#fffef8")

sidebar()
topbar()
mainframe()
update_sidebar()  #Update main existing diaries from the database

root.mainloop()
