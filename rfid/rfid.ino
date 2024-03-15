import mysql.connector
import os
import serial
import time
import tkinter as tk
from tkinter import ttk
from dotenv import load_dotenv

load_dotenv()

# Set up the serial connection (COM port may vary)
ser = serial.Serial(os.getenv('SERIAL_PORT'), 9600, timeout=1)
time.sleep(2)  # Wait for the connection to establish

# Function to check UID against the database
def check_uid_in_database(uid, doorName):
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'), 
        user=os.getenv('DB_USER'), 
        password=os.getenv('DB_PASSWORD'),  
        database=os.getenv('DB_NAME'),
        auth_plugin='mysql_native_password'
    )
    c = conn.cursor()

    # Check if the UID has access
    c.execute("SELECT Assoc_main_Accs, Assoc_office_Accs, Assoc_djroom_Accs FROM Assoc_info WHERE UID = %s", (uid,))
    row = c.fetchone()
    conn.close()

    if row:
        access_index = {'Main': 0, 'Office': 1, 'DJ Room': 2}
        if row[access_index[doorName]]:
            return '1'  # Access granted
    return '0'  # Access denied

# Function to insert information into the database
def insert_into_database(uid, std_dep, std_term, assoc_affil, assoc_dep, assoc_actv, assoc_main_accs, assoc_office_accs, assoc_djroom_accs, first_name, last_name, email, gsm, bday):
    # Connect tothe MySQL database
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'), 
        user=os.getenv('DB_USER'), 
        password=os.getenv('DB_PASSWORD'),  
        database=os.getenv('DB_NAME')  
    )
    c = conn.cursor()

    # Insert into School_info
    c.execute("INSERT INTO School_info (UID, Std_Dep, Std_Term) VALUES (%s, %s, %s)", (uid, std_dep, std_term))
    # Insert into Assoc_info
    c.execute("INSERT INTO Assoc_info (UID, Assoc_Affil, Assoc_Dep, Assoc_Actv, Assoc_main_Accs, Assoc_office_accs, Assoc_djroom_accs) VALUES (%s, %s, %s, %s, %s, %s, %s)", (uid, assoc_affil, assoc_dep, assoc_actv, assoc_main_accs, assoc_office_accs, assoc_djroom_accs))
    # Insert into Personal_info
    c.execute("INSERT INTO Personal_info (UID, FirstName, LastName, eMail, GSM, BDay) VALUES (%s, %s, %s, %s, %s, %s)", (uid, first_name, last_name, email, gsm, bday))

    conn.commit()
    conn.close()

# Function to handle form submission
def submit_form():
    uid = int(uid_entry.get())
    std_dep = std_dep_entry.get()
    std_term = int(std_term_entry.get())
    assoc_affil = assoc_affil_var.get()
    assoc_dep = assoc_dep_entry.get()
    assoc_actv = assoc_actv_var.get()
    assoc_main_accs = assoc_main_accs_var.get()
    assoc_office_accs = assoc_office_accs_var.get()
    assoc_djroom_accs = assoc_djroom_accs_var.get()
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    email = email_entry.get()
    gsm = int(gsm_entry.get())
    bday = bday_entry.get()

    insert_into_database(uid, std_dep, std_term, assoc_affil, assoc_dep, assoc_actv, assoc_main_accs, assoc_office_accs, assoc_djroom_accs, first_name, last_name, email, gsm, bday)

    # Clear form fields
    uid_entry.delete(0, tk.END)
    std_dep_entry.delete(0, tk.END)
    std_term_entry.delete(0, tk.END)
    assoc_affil_var.set(0)
    assoc_dep_entry.delete(0, tk.END)
    assoc_actv_var.set(0)
    assoc_main_accs_var.set(0)
    assoc_office_accs_var.set(0)
    assoc_djroom_accs_var.set(0)
    first_name_entry.delete(0, tk.END)
    last_name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    gsm_entry.delete(0, tk.END)
    bday_entry.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Add New User")

# Create form elements
uid_label = tk.Label(root, text="UID:")
uid_label.grid(row=0, column=0)
uid_entry = tk.Entry(root)
uid_entry.grid(row=0, column=1)

std_dep_label = tk.Label(root, text="Department:")
std_dep_label.grid(row=1, column=0)
std_dep_entry = tk.Entry(root)
std_dep_entry.grid(row=1, column=1)

std_term_label = tk.Label(root, text="Term:")
std_term_label.grid(row=2, column=0)
std_term_entry = tk.Entry(root)
std_term_entry.grid(row=2, column=1)

assoc_affil_label = tk.Label(root, text="Associate Affiliation:")
assoc_affil_label.grid(row=3, column=0)
assoc_affil_var = tk.IntVar()
assoc_affil_cb = tk.Checkbutton(root, variable=assoc_affil_var)
assoc_affil_cb.grid(row=3, column=1)

assoc_dep_label = tk.Label(root, text="Associate Department:")
assoc_dep_label.grid(row=4, column=0)
assoc_dep_entry = tk.Entry(root)
assoc_dep_entry.grid(row=4, column=1)

assoc_actv_label = tk.Label(root, text="Associate Active:")
assoc_actv_label.grid(row=5, column=0)
assoc_actv_var = tk.IntVar()
assoc_actv_cb = tk.Checkbutton(root, variable=assoc_actv_var)
assoc_actv_cb.grid(row=5, column=1)

assoc_main_accs_label = tk.Label(root, text="Main Access:")
assoc_main_accs_label.grid(row=6, column=0)
assoc_main_accs_var = tk.IntVar()
assoc_main_accs_cb = tk.Checkbutton(root, variable=assoc_main_accs_var)
assoc_main_accs_cb.grid(row=6, column=1)

assoc_office_accs_label = tk.Label(root, text="Office Access:")
assoc_office_accs_label.grid(row=7, column=0)
assoc_office_accs_var = tk.IntVar()
assoc_office_accs_cb = tk.Checkbutton(root, variable=assoc_office_accs_var)
assoc_office_accs_cb.grid(row=7, column=1)

assoc_djroom_accs_label = tk.Label(root, text="DJ Room Access:")
assoc_djroom_accs_label.grid(row=8, column=0)
assoc_djroom_accs_var = tk.IntVar()
assoc_djroom_accs_cb = tk.Checkbutton(root, variable=assoc_djroom_accs_var)
assoc_djroom_accs_cb.grid(row=8, column=1)

first_name_label = tk.Label(root, text="First Name:")
first_name_label.grid(row=9, column=0)
first_name_entry = tk.Entry(root)
first_name_entry.grid(row=9, column=1)

last_name_label = tk.Label(root, text="Last Name:")
last_name_label.grid(row=10, column=0)
last_name_entry = tk.Entry(root)
last_name_entry.grid(row=10, column=1)

email_label = tk.Label(root, text="Email:")
email_label.grid(row=11, column=0)
email_entry = tk.Entry(root)
email_entry.grid(row=11, column=1)

gsm_label = tk.Label(root, text="GSM:")
gsm_label.grid(row=12, column=0)
gsm_entry = tk.Entry(root)
gsm_entry.grid(row=12, column=1)

bday_label = tk.Label(root, text="Birthday (YYYY-MM-DD):")
bday_label.grid(row=13, column=0)
bday_entry = tk.Entry(root)
bday_entry.grid(row=13, column=1)

submit_button = tk.Button(root, text="Submit", command=submit_form)
submit_button.grid(row=14, column=0, columnspan=2)

# Main loop to listen for UIDs from the Arduino
while True:
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').strip().split(',')
        uid, doorName = data[0], data[1]  # Parse UID and door name from serial
        print(f'Received UID: {uid} for {doorName}')
        response = check_uid_in_database(uid, doorName)  # Check the UID against the database
        ser.write(response.encode())  # Send the response
        print(f'Sent response: {response}')

root.mainloop()