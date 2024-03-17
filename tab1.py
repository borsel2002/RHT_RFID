import tkinter as tk
from tkinter import messagebox
import serial

def lookup(ser):
    uid = get_uid(ser)
    if uid:
        # Perform lookup using the UID
        pass
    else:
        messagebox.showerror("Error", "Could not retrieve UID")

def get_uid(ser):
    global uid
    uid = None
    t = threading.Thread(target=receive_uid, args=(ser, tk.StringVar()))
    t.start()
    t.join()
    return uid