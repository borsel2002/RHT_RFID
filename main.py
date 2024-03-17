import tkinter as tk
from tkinter import messagebox
import pymysql
from pymysql.err import MySQLError
import serial
import os
import time
import threading
import tab1
import tab2

# Initialize the serial connection
ser = serial.Serial('/dev/tty/USB0', baudrate=9600, timeout=None)

# Create the main window
root = tk.Tk()

#Create tabs
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, columnspan=2)

# Tab 1: Lookup
tab1.create_tab1(notebook, ser)

# Tab 2: Add
tab2.create_tab2(notebook, ser)

root.mainloop()