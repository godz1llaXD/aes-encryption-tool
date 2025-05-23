# AES-256 Secure Encryption/Decryption with GUI, Password Change, Clipboard Copy
# Dependencies: pycryptodome, tkinter, pyperclip
# Install: pip install pycryptodome pyperclip

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import base64
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
import pyperclip

# === Parameters ===
iterations = 1000000
key_length = 32  # AES-256
session_password = None  # Global session password

# === Padding & Unpadding ===
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
        messagebox.showerror("Error", "No session password set.")
        return
    text = input_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Missing Input", "Please enter text to encrypt.")
        return
    try:
        encrypted = encrypt(text, session_password)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, encrypted)
        pyperclip.copy(encrypted)
        messagebox.showinfo("Encrypted", "Text encrypted and copied to clipboard.")
    except Exception as e:
        messagebox.showerror("Error", f"Encryption failed: {str(e)}")

def decrypt_gui():
    encrypted = input_text.get("1.0", tk.END).strip()
    if not encrypted:
        messagebox.showwarning("Missing Input", "Please enter encrypted text to decrypt.")
        return
    pwd = simpledialog.askstring("Decrypt", "Enter decryption password:", show="*")
    if not pwd:
        return
    try:
        decrypted = decrypt(encrypted, pwd)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, decrypted)
    except Exception:
        messagebox.showerror("Failed", "Decryption failed. Wrong password or bad data.")

def set_password():
    global session_password
    session_password = simpledialog.askstring("Set Password", "Enter encryption password:", show="*")
    if session_password:
        messagebox.showinfo("Password Set", "Encryption password set for this session.")

def change_password():
    global session_password
    old_pwd = simpledialog.askstring("Change Password", "Enter current password:", show="*")
    if old_pwd != session_password:
        messagebox.showerror("Incorrect", "Old password is incorrect.")
        return
    new_pwd = simpledialog.askstring("Change Password", "Enter new password:", show="*")
    confirm_pwd = simpledialog.askstring("Change Password", "Confirm new password:", show="*")
    if new_pwd != confirm_pwd:
        messagebox.showerror("Mismatch", "New passwords do not match.")
    else:
        session_password = new_pwd
        messagebox.showinfo("Changed", "Password changed successfully.")

# === GUI Layout ===
root = tk.Tk()
root.title("AES-256 Encryptor")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

tk.Label(frame, text="Input Message / Encrypted Text:").pack()
input_text = scrolledtext.ScrolledText(frame, height=8, width=70)
input_text.pack()

tk.Label(frame, text="Output:").pack()
output_text = scrolledtext.ScrolledText(frame, height=8, width=70)
output_text.pack()

btn_frame = tk.Frame(frame)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Encrypt", width=15, command=encrypt_gui).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Decrypt", width=15, command=decrypt_gui).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Set Password", width=15, command=set_password).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Change Password", width=15, command=change_password).grid(row=0, column=3, padx=5)

root.mainloop()
