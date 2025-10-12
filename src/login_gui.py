# login_gui.py
import tkinter as tk
from tkinter import messagebox
import database  # your existing database.py

# -----------------------------
# FUNCTIONS
# -----------------------------

def register_user():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    if not username or not password:
        messagebox.showwarning("Warning", "Please enter both username and password")
        return

    # Attempt to register user
    result = database.register_user(username, password)
    if result:
        messagebox.showinfo("Success", "User registered successfully!")
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        launch_jarvis()  # Launch Jarvis GUI after registration
    else:
        messagebox.showerror("Error", "User already exists!")

def login_user():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    if not username or not password:
        messagebox.showwarning("Warning", "Please enter both username and password")
        return

    # Attempt login
    result = database.login_user(username, password)
    if result:
        messagebox.showinfo("Success", "Login successful!")
        launch_jarvis()  # Launch Jarvis GUI after login
    else:
        messagebox.showerror("Error", "Invalid username or password")

def launch_jarvis():
    # Close login window first
    root.destroy()

    # -----------------------------
    # Import the updated Jarvis GUI
    # -----------------------------
    import jarvis_gui

    # Start Jarvis main GUI loop
    jarvis_gui.main()  # Ensure jarvis_gui.py has main() function at the end

# -----------------------------
# GUI SETUP
# -----------------------------

root = tk.Tk()
root.title("Jarvis Login")
root.geometry("400x250")

# Username
tk.Label(root, text="Username:").pack(pady=(20, 5))
username_entry = tk.Entry(root, font=("Arial", 14))
username_entry.pack(pady=5)

# Password
tk.Label(root, text="Password:").pack(pady=(10, 5))
password_entry = tk.Entry(root, font=("Arial", 14), show="*")
password_entry.pack(pady=5)

# Buttons
tk.Button(root, text="Login", font=("Arial", 12), command=login_user).pack(pady=(15, 5))
tk.Button(root, text="Register", font=("Arial", 12), command=register_user).pack(pady=5)

root.mainloop()
