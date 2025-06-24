'''This is what the regular diary entry
will look like. This is all GUI (for now) and 
will link through the randomized aspect of the daily diary 
prompts'''

from tkinter import *
import webbrowser
import tkinter as tk
from tkinter import messagebox

# Root window
root = tk.Tk()
root.title("Diary App")
root.geometry("1000x600")
root.configure(bg="#fdfaf2")

# Sidebar
sidebar = tk.Frame(root, bg="#f7f3e7", width=200)
sidebar.pack(side="left", fill="y")

tk.Label(sidebar, text="Your Account", bg="#f7f3e7", font=("Arial", 10)).pack(pady=(10, 5))
tk.Canvas(sidebar, width=50, height=50, bg="#f7f3e7", highlightthickness=1, highlightbackground="gray").pack(pady=5)

tk.Label(sidebar, text="Home", bg="#f7f3e7", fg="#b47e50", font=("Arial", 12)).pack(pady=(20, 2), anchor="w", padx=10)
tk.Label(sidebar, text="My Diaries", bg="#f7f3e7", fg="#a55d27", font=("Arial", 12, "bold")).pack(pady=(5, 2), anchor="w", padx=10)
tk.Label(sidebar, text="> Summer '24", bg="#f7f3e7", font=("Arial", 10)).pack(anchor="w", padx=20)
tk.Label(sidebar, text="> My Everyday", bg="#f7f3e7", font=("Arial", 10)).pack(anchor="w", padx=20)

root.mainloop()