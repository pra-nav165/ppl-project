import os
import customtkinter as ctk
import mysql.connector
from tkinter import filedialog, messagebox
from encryption import encrypt_text_file
from decryption import decrypt_text_file
from backend import create_connection, insert_user, user_exists, fetch_random_characters

# Initialize the application
app = ctk.CTk()

# Set the title and geometry
app.title("File Encryption and Decryption")
app.geometry("400x300")

# Database connection
connection = create_connection()

# Function to handle registration
def register_user():
    username = username_entry.get()
    password = password_entry.get()
    if validate_password(password):
        insert_user(connection, username, password)
        messagebox.showinfo("Success", "User registered successfully!")
    else:
        messagebox.showerror("Error", "Password must contain at least one uppercase letter, one special character, one number, and be at least 6 characters long.")

# Function to handle login
def login_user():
    username = login_username_entry.get()
    password = login_password_entry.get()
    if user_exists(connection, username, password):
        open_file_action_window(username)
    else:
        messagebox.showerror("Error", "Invalid username or password.")

# Function to validate password
def validate_password(password):
    import re
    regex = re.compile(r'^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9]).{6,}$')
    return re.match(regex, password)

# Function to handle file actions (encrypt/decrypt)
def open_file_action_window(username):
    file_action_window = ctk.CTkToplevel(app)
    file_action_window.title("File Actions")
    file_action_window.geometry("400x200")

    def encrypt_file():
        file_path = filedialog.askopenfilename()
        if file_path:
            output_filepath = file_path + ".enc"
            encrypt_text_file(username, file_path, output_filepath)
            messagebox.showinfo("Success", f"File encrypted successfully! Saved as {output_filepath}")

    def decrypt_file():
        file_path = filedialog.askopenfilename()
        if file_path:
            output_filepath = file_path + ".dec"
            decrypt_text_file(username, file_path, output_filepath)
            messagebox.showinfo("Success", f"File decrypted successfully! Saved as {output_filepath}")

    encrypt_button = ctk.CTkButton(file_action_window, text="Encrypt File", command=encrypt_file)
    encrypt_button.pack(pady=10)

    decrypt_button = ctk.CTkButton(file_action_window, text="Decrypt File", command=decrypt_file)
    decrypt_button.pack(pady=10)

# Registration Frame
register_frame = ctk.CTkFrame(app)
register_frame.pack(pady=10)

username_label = ctk.CTkLabel(register_frame, text="Username:")
username_label.pack()
username_entry = ctk.CTkEntry(register_frame)
username_entry.pack()

password_label = ctk.CTkLabel(register_frame, text="Password:")
password_label.pack()
password_entry = ctk.CTkEntry(register_frame, show="*")
password_entry.pack()

register_button = ctk.CTkButton(register_frame, text="Register", command=register_user)
register_button.pack(pady=10)

# Login Frame
login_frame = ctk.CTkFrame(app)
login_frame.pack(pady=10)

login_username_label = ctk.CTkLabel(login_frame, text="Username:")
login_username_label.pack()
login_username_entry = ctk.CTkEntry(login_frame)
login_username_entry.pack()

login_password_label = ctk.CTkLabel(login_frame, text="Password:")
login_password_label.pack()
login_password_entry = ctk.CTkEntry(login_frame, show="*")
login_password_entry.pack()

login_button = ctk.CTkButton(login_frame, text="Login", command=login_user)
login_button.pack(pady=10)

# Run the application
app.mainloop()
