'''This version is the version in which I will be adding a database to the 
homepagae. This makes saving files and newly made 
"diary" folders easier. '''

import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import sqlite3
import sys
import os
from tkinter import messagebox
from datetime import datetime

#Adding a main database
db_file = "diary_app.db"

#Reads user_id from login script.
if len(sys.argv) > 1:
    current_user_id = int(sys.argv[1])
else:
    current_user_id = 1  #Default user ID for testing.

print(f"[DEBUG] current_user_id at startup = {current_user_id}")

#-------------- DATABASE --------------

def init_db():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    #Users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                      )''')

    #Diaries table
    cursor.execute('''CREATE TABLE IF NOT EXISTS diaries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        title TEXT NOT NULL,
                        description TEXT,
                        image TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id)
                      )''')

    #Entries table
    cursor.execute('''CREATE TABLE IF NOT EXISTS diary_entries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        diary_id INTEGER NOT NULL,
                        entry_date TEXT NOT NULL,
                        content TEXT NOT NULL,
                        FOREIGN KEY(diary_id) REFERENCES diaries(id)
                      )''')

    conn.commit()
    conn.close()


def insert_diary(user_id, title, description, image):
    '''Insert new diary entry'''

    if user_id is None:
        print("No user logged in. Cannot insert diary.")
        return

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO diaries (user_id, title, description, image) VALUES (?, ?, ?, ?)",
        (user_id, title, description, image)
    )
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

def get_entries_by_diary_id(diary_id):
    '''Fetch all entries for a specific diary, ordered by date.'''
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT entry_date, content FROM diary_entries WHERE diary_id=? ORDER BY entry_date DESC",
        (diary_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

# ---------------- GUI SETUP ----------------
sidebar_buttons = []
current_diary_frame = None
main_frame = None     #Keep track of the main frame to refresh when needed.

def add_diary():
    '''Create a new diary entry window'''

    def submit_diary():
        global current_user_id
        title = title_entry.get()
        description = description_entry.get("1.0", "end-1c")
        image_path = image_path_var.get()

        if not title:
            print("Please enter a title.")  #Optional warning
            return

        #Save to database using current_user_id.
        insert_diary(current_user_id, title, description, image_path)
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
                                 fg_color="#7c5b44", text_color="#fffef8",
                                hover_color="#b59a90", width=210, font=("Verdana", 12))
    image_button.place(relx=0.42, rely=0.55)

    submit_button = ctk.CTkButton(new_window, text="Add Diary", command=submit_diary,
                                  fg_color="#7c5b44", text_color="#fffef8",
                                hover_color="#b59a90", width=210, font=("Verdana", 12))
    submit_button.place(relx=0.42, rely=0.65)


def get_user_diaries(user_id):

    '''Return all diaries belonging to a specific user.'''

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, image FROM diaries WHERE user_id=?", (user_id,))
    diaries = cursor.fetchall()
    conn.close()
    return diaries

def update_sidebar():

    '''Updating the diaries that can be found on the side
    bar'''

    for btn in sidebar_buttons:
        btn.destroy()
    sidebar_buttons.clear()

    if current_user_id is None:
        return  #No user logged in.

    diaries = get_user_diaries(current_user_id)  #Filters by logged in users.
    for idx, diary in enumerate(diaries):
        diary_id, title, image = diary
        btn = ctk.CTkButton(root, text=title, font=("Verdana", 14),
                            fg_color="#7c5b44", width=100,
                            text_color="#fffef8", hover_color="#b59a90",
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

    if main_frame:
        main_frame.destroy()

    if current_diary_frame:
        current_diary_frame.destroy()

    current_diary_frame = ctk.CTkFrame(root, fg_color="#fffef8")
    current_diary_frame.place(relx=0.155, rely=0.156, relwidth=0.845, relheight=0.845)

    def go_back():

        global current_diary_frame
        current_diary_frame.destroy()
        current_diary_frame = None #Resets so the diaries can be clicked again.
        mainframe()  #Reloads main "My Diaries" frame
        update_sidebar()

    back_button = ctk.CTkButton(current_diary_frame,
                                text="Back",
                                command=go_back,
                                fg_color="#7c5b44",
                                text_color="#fffef8",
                                hover_color="#b59a90",
                                width=100,
                                height=35,
                                corner_radius=8)
    back_button.place(relx=0.02, rely=0.02)

    title_label = ctk.CTkLabel(current_diary_frame, text=title, font=("Verdana", 36),
                               fg_color="#fffef8", text_color="#9d7757")
    title_label.place(relx=0.05, rely=0.1)

    if image_path:
        try:
            img = Image.open(image_path)
            img = img.resize((300, 300), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)
            img_label = ctk.CTkLabel(current_diary_frame, 
                                     image=img, 
                                     text="",
                                     fg_color="#fffef8")
            img_label.image = img
            img_label.place(relx=0.05, rely=0.2)
        except:
            pass

    description_label = ctk.CTkLabel(current_diary_frame, text=description,
                                     font=("Verdana", 14), fg_color="#fffef8", wraplength=800)
    description_label.place(relx=0.4, rely=0.2)

    entries = get_entries_by_diary_id(diary_id)

    if entries:
        entries_frame = ctk.CTkFrame(current_diary_frame, fg_color="#f9f6f1", corner_radius=8)
        entries_frame.place(relx=0.05, rely=0.55, relwidth=0.9, relheight=0.4)

        entries_label = ctk.CTkLabel(entries_frame, text="Entries:",
                                     font=("Verdana", 20, "bold"),
                                     text_color="#7c5b44")
        entries_label.place(relx=0.02, rely=0.02)

        #Scrollable container for entries
        canvas = ctk.CTkCanvas(entries_frame, bg="#f9f6f1", highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(entries_frame, command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas, fg_color="#f9f6f1")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.place(relx=0, rely=0.1, relwidth=0.95, relheight=0.85)
        scrollbar.place(relx=0.95, rely=0.1, relheight=0.85)

        current_y = 0.0
        for entry_date, content in entries:
            entry_frame = ctk.CTkFrame(scrollable_frame, fg_color="#fffef8", corner_radius=8)
            entry_frame.pack(fill="x", pady=5, padx=10)

            date_label = ctk.CTkLabel(entry_frame, text=entry_date,
                                      font=("Verdana", 10),
                                      text_color="#9d7757")
            date_label.pack(anchor="w", padx=10, pady=2)

            content_label = ctk.CTkLabel(entry_frame, text=content,
                                         font=("Verdana", 14),
                                         wraplength=700,
                                         text_color="#4b3b33",
                                         justify="left")
            content_label.pack(anchor="w", padx=10, pady=5)
    else:
        no_entries_label = ctk.CTkLabel(current_diary_frame,
                                        text="No entries yet for this diary.",
                                        font=("Verdana", 14),
                                        text_color="#9d7757")
        no_entries_label.place(relx=0.05, rely=0.55)

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
        image1 = "blue_logo.png"
        image = Image.open(image1)
        image = image.resize((135, 135), Image.Resampling.LANCZOS)
        icon_image = ImageTk.PhotoImage(image)

        icon_label = ctk.CTkLabel(top_bar, image=icon_image, text="")
        icon_label.image = icon_image
        icon_label.place(relx=0, rely=0, relwidth=0.1, relheight=1)
    except:
        pass

def mainframe():
    '''Main frame in the root'''
    global main_frame
    if main_frame:  #Destroy if already exists.
        main_frame.destroy()

    main_frame = ctk.CTkFrame(root, fg_color="#fffef8")
    main_frame.place(relx=0.155, rely=0.156, relwidth=0.845, relheight=0.845)

    my_diaries_label = ctk.CTkLabel(main_frame,
                                    text="My Diaries",
                                    font=("Helvetica", 56, "bold"), fg_color="#fffef8",
                                    text_color="#9d7757")
    my_diaries_label.place(relx=0.08, rely=0.12)

    new_entry_button = ctk.CTkButton(main_frame,
                                     text="New Entry",
                                     font=("Verdana", 16),
                                     fg_color="#7c5b44",
                                     text_color="#fffef8",
                                     hover_color="#b59a90",
                                     command=open_new_entry_window)
    new_entry_button.place(relx=0.85, rely=0.05)

    add_new_diary_frame = ctk.CTkFrame(main_frame,
                                       fg_color="#fffef8",
                                       border_width=2, border_color="#9d7757")
    add_new_diary_frame.place(relx=0.08, rely=0.35, relheight=0.54, relwidth=0.24)

    add_diary_button = ctk.CTkButton(add_new_diary_frame, text="+",
                                     font=("Helvetica", 50), fg_color="#fffef8",
                                     text_color="#bed0d4", hover_color="#dae7e9", border_color="#a89885",
                                     command=add_diary, border_width=2, width=90, height=90)
    add_diary_button.place(relx=0.32, rely=0.38)
    
#Pop up window to add new diary entry.
def open_new_entry_window():

    '''Open a pop-up window to create a new diary entry'''

    new_entry_win = ctk.CTkToplevel(root)
    new_entry_win.title("New Entry")
    new_entry_win.geometry("900x700")
    new_entry_win.configure(fg_color="#fffef8")

    #Dropdown to select which diary the entry belongs to.
    diaries = get_user_diaries(current_user_id)
    diary_titles = [d[1] for d in diaries] if diaries else ["No Diaries Found"]
    diary_ids = [d[0] for d in diaries] if diaries else []
    selected_diary = ctk.StringVar(value=diary_titles[0])

    diary_label = ctk.CTkLabel(new_entry_win, text="Select Diary:",
                               font=("Verdana", 16),
                               fg_color="#fffef8",
                               text_color="#7c5b44")
    diary_label.place(relx=0.05, rely=0.05)

    diary_dropdown = ctk.CTkOptionMenu(new_entry_win,
                                       variable=selected_diary,
                                       values=diary_titles,
                                       fg_color="#d8cab6",
                                       text_color="#7c5b44",
                                       width=250)
    diary_dropdown.place(relx=0.25, rely=0.05)

    #Large scrollable textbox for writing.
    text_frame = ctk.CTkFrame(new_entry_win, 
                              fg_color="#fffef8", border_width=1, 
                              border_color="#a89885")
    text_frame.place(relx=0.05, rely=0.15, relwidth=0.9, relheight=0.65)

    entry_textbox = ctk.CTkTextbox(text_frame, wrap="word", font=("Verdana", 14))
    entry_textbox.place(relx=0, rely=0, relwidth=0.95, relheight=1)

    scrollbar = ctk.CTkScrollbar(text_frame, command=entry_textbox.yview)
    scrollbar.place(relx=0.95, rely=0, relheight=1)
    entry_textbox.configure(yscrollcommand=scrollbar.set)

    def save_entry():
        from datetime import datetime
        if not diary_ids:
            print("No diaries exist to save this entry.")
            return
        diary_index = diary_titles.index(selected_diary.get())
        diary_id = diary_ids[diary_index]
        content = entry_textbox.get("1.0", "end-1c").strip()

        if not content:
            messagebox.showwarning("Empty Entry", "Diary entry cannot be empty before saving.")
            return

        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO diary_entries (diary_id, entry_date, content) VALUES (?, ?, ?)",
            (diary_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), content)
        )
        conn.commit()
        conn.close()
        print("Entry saved successfully.")
        new_entry_win.destroy()
    

    save_button = ctk.CTkButton(new_entry_win, text="Save Entry",
                                fg_color="#aabfc4", text_color="#fffef8",
                                hover_color="#c9dbdd",
                                command=save_entry)
    save_button.place(relx=0.72, rely=0.9)

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
