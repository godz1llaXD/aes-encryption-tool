# AES-256 Encrypt/Decrypt GUI with Password Prompt on Startup
# Install with: pip install pycryptodome pyperclip

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import base64
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
import pyperclip
import sys

# === Constants ===
iterations = 1000000
key_length = 32
session_password = None  # Will be assigned at startup

# === Padding helpers ===
def pad(msg):
    pad_len = 16 - len(msg.encode()) % 16
    return msg + chr(pad_len) * pad_len

def unpad(msg):
    pad_len = msg[-1]
    return msg[:-pad_len]

# === Encryption ===
def encrypt(plaintext, password):
    salt = get_random_bytes(16)
    iv = get_random_bytes(16)
    key = PBKDF2(password, salt, dkLen=key_length, count=iterations)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad(plaintext)
    ciphertext = cipher.encrypt(padded.encode())
    payload = salt + iv + ciphertext
    return base64.b64encode(payload).decode()

# === Decryption ===
def decrypt(b64_data, password):
    raw = base64.b64decode(b64_data)
    salt, iv, ciphertext = raw[:16], raw[16:32], raw[32:]
    key = PBKDF2(password, salt, dkLen=key_length, count=iterations)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)
    return unpad(decrypted).decode()

# === GUI Actions ===
def encrypt_gui():
    global session_password
    if not session_password:
        messagebox.showerror("Error", "No session password set.", parent=root)
        return
    text = input_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Missing Input", "Please enter text to encrypt.", parent=root)
        return
    try:
        encrypted = encrypt(text, session_password)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, encrypted)
        pyperclip.copy(encrypted)
        messagebox.showinfo("Encrypted", "Text encrypted and copied to clipboard.", parent=root)
    except Exception as e:
        messagebox.showerror("Error", f"Encryption failed: {str(e)}", parent=root)

def decrypt_gui():
    encrypted = input_text.get("1.0", tk.END).strip()
    if not encrypted:
        messagebox.showwarning("Missing Input", "Please enter encrypted text to decrypt.", parent=root)
        return
    pwd = simpledialog.askstring("Decrypt", "Enter decryption password:", show="*", parent=root)
    if not pwd:
        return
    try:
        decrypted = decrypt(encrypted, pwd)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, decrypted)
    except Exception:
        messagebox.showerror("Failed", "Decryption failed. Wrong password or bad data.", parent=root)

def set_password():
    global session_password
    session_password = simpledialog.askstring("Set Password", "Enter encryption password:", show="*", parent=root)
    if session_password:
        messagebox.showinfo("Password Set", "Session password set successfully.", parent=root)

def change_password():
    global session_password
    old_pwd = simpledialog.askstring("Change Password", "Enter current password:", show="*", parent=root)
    if old_pwd != session_password:
        messagebox.showerror("Incorrect", "Old password is incorrect.", parent=root)
        return
    new_pwd = simpledialog.askstring("Change Password", "Enter new password:", show="*", parent=root)
    confirm_pwd = simpledialog.askstring("Change Password", "Confirm new password:", show="*", parent=root)
    if new_pwd != confirm_pwd:
        messagebox.showerror("Mismatch", "New passwords do not match.", parent=root)
    else:
        session_password = new_pwd
        messagebox.showinfo("Changed", "Password changed successfully.", parent=root)

# === Initialize GUI ===
root = tk.Tk()
root.title("AES-256 Encryptor")
root.geometry("700x600")

# Bring window to front briefly
root.lift()
root.attributes("-topmost", True)
root.after(500, lambda: root.attributes("-topmost", False))

# Ask for session password before continuing
while not session_password:
    session_password = simpledialog.askstring("Startup Password", "Set session password to begin:", show="*", parent=root)
    if not session_password:
        confirm = messagebox.askyesno("Exit?", "No password set. Exit application?", parent=root)
        if confirm:
            sys.exit()

# === Layout ===
frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

tk.Label(frame, text="Input Message / Encrypted Text:").pack()
input_text = scrolledtext.ScrolledText(frame, height=8, width=80)
input_text.pack()

tk.Label(frame, text="Output:").pack()
output_text = scrolledtext.ScrolledText(frame, height=8, width=80)
output_text.pack()

btn_frame = tk.Frame(frame)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Encrypt", width=15, command=encrypt_gui).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Decrypt", width=15, command=decrypt_gui).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Set Password", width=15, command=set_password).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Change Password", width=15, command=change_password).grid(row=0, column=3, padx=5)

root.mainloop()
