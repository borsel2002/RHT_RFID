import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox
import os
from dotenv import load_dotenv
import time
import serial

# Set up the serial connection (COM port may vary)
ser = serial.Serial('COM11', baudrate=9600, timeout=None)
time.sleep(0.01)  # Wait for the connection to establish

def main():
    global uid

    # Main loop to listen for UIDs from the Arduino
    data = ser.readline().decode('utf-8').strip().split(',')
    uid, doorName = data[0], data[1]  # Parse UID and door name from serial input

    # Create a function to insert data into the database
    def insert_into_database(uid, std_id, std_dep, std_term, assoc_affil, assoc_dep, assoc_actv, assoc_main_accs, assoc_office_accs, assoc_djroom_accs, first_name, last_name, email, gsm, bday):
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'), 
            user=os.getenv('DB_USER'), 
            password=os.getenv('DB_PASSWORD'),  
            database=os.getenv('DB_NAME'),
            auth_plugin='mysql_native_password'  
        )
        c = conn.cursor()

        # Insert into School_info
        c.execute("INSERT INTO School_info (Std_ID, Std_Dep, Std_Term, UID) VALUES (%s, %s, %s, %s)", (std_id, std_dep, std_term, uid))

        # Insert into Assoc_info
        c.execute("INSERT INTO Assoc_info (Assoc_Affil, Assoc_Dep, Assoc_Actv, Assoc_main_Accs, Assoc_office_Accs, Assoc_djroom_Accs, Std_ID) VALUES (%s, %s, %s, %s, %s, %s, %s)", (assoc_affil, assoc_dep, assoc_actv, assoc_main_accs, assoc_office_accs, assoc_djroom_accs, std_id))

        # Insert into Personal_info
        c.execute("INSERT INTO Personal_info (FirstName, LastName, eMail, GSM, BDay, Std_ID) VALUES(%s, %s, %s, %s, %s, %s)", (first_name, last_name, email, gsm, bday, std_id))

        conn.commit()
        conn.close()

    # Function to handle form submission
    def submit_form(std_id_entry, std_dep_entry, std_term_entry, assoc_affil_var, assoc_dep_entry, assoc_actv_var, assoc_main_accs_var, assoc_office_accs_var, assoc_djroom_accs_var, first_name_entry, last_name_entry, email_entry, gsm_entry, bday_entry):
        std_id = std_id_entry.get()
        std_dep = std_dep_entry.get()
        std_term = int(std_term_entry.get())
        assoc_affil = assoc_affil_var.get()
        assoc_dep = assoc_dep_entry.get()
        assoc_actv = assoc_actv_var.get()
        assoc_main_accs = assoc_main_accs_var.get()
        assoc_office_accs = assoc_office_accs_var.get()
        assoc_djroom_accs = assoc_djroom_accs_var.get()
        first_name = first_name_entry.get()
        last_name= last_name_entry.get()
        email = email_entry.get()
        gsm = int(gsm_entry.get())
        bday = bday_entry.get()

        insert_into_database(uid, std_id, std_dep, std_term, assoc_affil, assoc_dep, assoc_actv, assoc_main_accs, assoc_office_accs, assoc_djroom_accs, first_name, last_name, email, gsm, bday)

        # Clear form fields
        uid_entry.delete(0, tk.END)
        std_id_entry.delete(0, tk.END)
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

        # Close the form
        form.destroy()

    # Create the main window
    root = tk.Tk()

    # Create form elements
    uid_label = tk.Label(root, text="UID:")
    uid_label.grid(row=0, column=0)
    uid_label = tk.Label(root, text=(uid))
    uid_label.grid(row=0, column=1)

    std_id_label = tk.Label(root, text="Student ID:")
    std_id_label.grid(row=1, column=0)
    std_id_entry = tk.Entry(root)
    std_id_entry.grid(row=1, column=1)

    std_dep_label = tk.Label(root, text="Department:")
    std_dep_label.grid(row=2, column=0)
    std_dep_entry = tk.Entry(root)
    std_dep_entry.grid(row=2, column=1)

    std_term_label = tk.Label(root, text="Term:")
    std_term_label.grid(row=3, column=0)
    std_term_entry = tk.Entry(root)
    std_term_entry.grid(row=3, column=1)

    assoc_affil_label = tk.Label(root, text="Associate Affiliation:")
    assoc_affil_label.grid(row=4, column=0)
    assoc_affil_var = tk.IntVar()
    assoc_affil_cb = tk.Checkbutton(root, variable=assoc_affil_var)
    assoc_affil_cb.grid(row=4, column=1)

    assoc_dep_label = tk.Label(root, text="Associate Department:")
    assoc_dep_label.grid(row=5, column=0)
    assoc_dep_entry = tk.Entry(root)
    assoc_dep_entry.grid(row=5, column=1)

    assoc_actv_label = tk.Label(root, text="Associate Active:")
    assoc_actv_label.grid(row=6, column=0)
    assoc_actv_var = tk.IntVar()
    assoc_actv_cb = tk.Checkbutton(root, variable=assoc_actv_var)
    assoc_actv_cb.grid(row=6, column=1)

    assoc_main_accs_label = tk.Label(root, text="Main Access:")
    assoc_main_accs_label.grid(row=7, column=0)
    assoc_main_accs_var = tk.IntVar()
    assoc_main_accs_cb = tk.Checkbutton(root, variable=assoc_main_accs_var)
    assoc_main_accs_cb.grid(row=7,column=1)

    assoc_office_accs_label = tk.Label(root, text="Office Access:")
    assoc_office_accs_label.grid(row=8, column=0)
    assoc_office_accs_var = tk.IntVar()
    assoc_office_accs_cb = tk.Checkbutton(root, variable=assoc_office_accs_var)
    assoc_office_accs_cb.grid(row=8, column=1)

    assoc_djroom_accs_label = tk.Label(root, text="DJ Room Access:")
    assoc_djroom_accs_label.grid(row=9, column=0)
    assoc_djroom_accs_var = tk.IntVar()
    assoc_djroom_accs_cb = tk.Checkbutton(root, variable=assoc_djroom_accs_var)
    assoc_djroom_accs_cb.grid(row=9, column=1)

    first_name_label = tk.Label(root, text="First Name:")
    first_name_label.grid(row=10, column=0)
    first_name_entry = tk.Entry(root)
    first_name_entry.grid(row=10, column=1)

    last_name_label = tk.Label(root, text="Last Name:")
    last_name_label.grid(row=11, column=0)
    last_name_entry = tk.Entry(root)
    last_name_entry.grid(row=11, column=1)

    email_label= tk.Label(root, text="Email:")
    email_label.grid(row=12, column=0)
    email_entry = tk.Entry(root)
    email_entry.grid(row=12, column=1)

    gsm_label = tk.Label(root, text="GSM:")
    gsm_label.grid(row=13, column=0)
    gsm_entry = tk.Entry(root)
    gsm_entry.grid(row=13, column=1)

    bday_label = tk.Label(root, text="Birthday (YYYY-MM-DD):")
    bday_label.grid(row=14, column=0)
    bday_entry = tk.Entry(root)
    bday_entry.grid(row=14, column=1)

    # Button to submit the form
    submit_button = tk.Button(root, text="Submit", command=lambda: submit_form(std_id_entry, std_dep_entry, std_term_entry, assoc_affil_var, assoc_dep_entry, assoc_actv_var, assoc_main_accs_var, assoc_office_accs_var, assoc_djroom_accs_var, first_name_entry, last_name_entry, email_entry, gsm_entry, bday_entry))
    submit_button.grid(row=15, column=0, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    main()