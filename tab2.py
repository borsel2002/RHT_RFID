import tkinter as tk
from tkinter import messagebox
import pymysql
from pymysql.err import MySQLError
import serial
import os
import time
import threading

def submit_form(ser):
    uid = get_uid(ser)
    if uid:
        # Get form data
        std_id = get_std_id()
        std_dep = get_std_dep()
        std_term = get_std_term()
        assoc_affil = get_assoc_affil()
        assoc_dep = get_assoc_dep()
        assoc_actv = get_assoc_actv()

        # Submit form data to the database
        submit_to_db(std_id, std_dep, std_term, uid, assoc_affil, assoc_dep, assoc_actv)
    else:
        messagebox.showerror("Error", "Could not retrieve UID")

def get_uid(ser):
    global uid
    uid = None
    t = threading.Thread(target=receive_uid, args=(ser, tk.StringVar()))
    t.start()
    t.join()
    return uid

def receive_uid(ser, uid_var):
    global uid
    while True:
        data = ser.readline().decode('utf-8').strip().split(',')
        uid, doorName = data[0], data[1]  # Parse UID and door name from serial input
        if uid:
            uid_var.set(uid)
            break

def get_std_id():
    # Get standard ID input
    std_id_entry = tk.Entry(tab2)
    std_id_entry.grid(row=0, column=0, columnspan=2)
    return std_id_entry.get()

def get_std_dep():
    # Get standard department input
    std_dep_entry = tk.Entry(tab2)
    std_dep_entry.grid(row=1, column=0, columnspan=2)
    return std_dep_entry.get()

def get_std_term():
    # Get standard term input
    std_term_entry = tk.Entry(tab2)
    std_term_entry.grid(row=2, column=0, columnspan=2)
    return std_term_entry.get()

def get_assoc_affil():
    # Get associated affiliation input
    assoc_affil_entry = tk.Entry(tab2)
    assoc_affil_entry.grid(row=3, column=0, columnspan=2)
    return assoc_affil_entry.get()

def get_assoc_dep():
    # Get associated department input
    assoc_dep_entry = tk.Entry(tab2)
    assoc_dep_entry.grid(row=4, column=0, columnspan=2)
    return assoc_dep_entry.get()

def get_assoc_actv():
    # Get associated activity input
    assoc_actv_entry = tk.Entry(tab2)
    assoc_actv_entry.grid(row=5, column=0, columnspan=2)
    return assoc_actv_entry.get()

def submit_to_db(std_id, std_dep, std_term, uid, assoc_affil, assoc_dep, assoc_actv):
    try:
        # Connect to the database
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="password",
            db="mydatabase"
        )

        # Create a cursor object
        cursor = connection.cursor()

        # Execute the SQL query
        cursor.execute(
            "INSERT INTO mytable (std_id, std_dep, std_term, uid, assoc_affil, assoc_dep, assoc_actv) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (std_id, std_dep, std_term, uid, assoc_affil, assoc_dep, assoc_actv)
        )

        # Commit the transaction
        connection.commit()

        # Close the cursor and the connection
        cursor.close()
        connection.close()

        messagebox.showinfo("Success", "Form submitted successfully")

    except MySQLError as e:
        messagebox.showerror("Error", f"Could not submit form: {e}")