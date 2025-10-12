# login_gui.py
import tkinter as tk
from tkinter import messagebox
import sqlite3

# ----------------------------
# DATABASE SETUP
# ----------------------------
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY
)
''')
conn.commit()

# ----------------------------
# GUI
# ----------------------------
root = tk.Tk()
root.title("Login")
root.geometry("400x200")

tk.Label(root, text="Username:").pack(pady=10)
username_entry = tk.Entry(root)
username_entry.pack(pady=5)
username_entry.focus()

def login_user():
    username = username_entry.get().strip()
    if not username:
        messagebox.showerror("Error", "Please enter username")
        return

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    data = cursor.fetchone()
    if not data:
        # Add new user
        cursor.execute("INSERT INTO users VALUES (?)", (username,))
        conn.commit()

    messagebox.showinfo("Success", f"Welcome {username}!")
    launch_jarvis()

def launch_jarvis():
    # Close login window
    root.destroy()
    # Import and launch Jarvis GUI
    import jarvis_gui
    jarvis_gui.main()  # main() function must exist in jarvis_gui.py

tk.Button(root, text="Login", command=login_user).pack(pady=20)

root.mainloop()
