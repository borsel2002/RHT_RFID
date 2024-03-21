import pymysql
from pymysql.err import MySQLError
import tkinter as tk
from tkinter import messagebox
import os
import time
import serial
from tkinter import ttk
import threading

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
    last_name = last_name_entry.get()
    email = email_entry.get()
    gsm = int(gsm_entry.get())
    bday = bday_entry.get()

    if uid:
        try:
            # Connect to the MySQL database
            conn = pymysql.connect(
                host=os.getenv('DB_HOST'), 
                user=os.getenv('DB_USER'), 
                password=os.getenv('DB_PASSWORD'),  database=os.getenv('DB_NAME')  
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

            # Clear form fields
            std_id_entry.delete(0, tk.END)
            std_dep_entry.delete(0, tk.END)
            assoc_main_accs_var.set(0)
            assoc_office_accs_var.set(0)
            assoc_djroom_accs_var.set(0)
            first_name_entry.delete(0, tk.END)
            last_name_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
            gsm_entry.delete(0, tk.END)
            bday_entry.delete(0, tk.END)
            std_term_entry.delete(0, tk.END)        
            assoc_affil_var.set(0)
            assoc_affil_var.set(0)
            assoc_dep_entry.delete(0, tk.END)
            assoc_actv_var.set(0)
            assoc_main_accs_var.set(0)
            assoc_office_accs_var.set(0)
            assoc_djroom_accs_var.set(0)
            first_name_entry.delete(0, tk.END)

        except MySQLError as e:
            messagebox.showerror("Error", f"Could not insert into database: {e}")

def setup_serial_connection():
    try:
        ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=None)
        time.sleep(0.01)  # Wait for the connection to establish
        return ser
    except serial.SerialException as e:
        messagebox.showerror("Error", f"Could not connect to serial device: {e}")
        return None

def receive_uid(ser):
    global uid
    while True:
        data = ser.readline().decode('utf-8').strip().split(',')
        uid, doorName = data[0], data[1]  # Parse UID and door name from serial input
        if uid:
            break

def main():
    global uid
    ser = setup_serial_connection()
    if ser:
        t = threading.Thread(target=receive_uid, args=(ser,))
        t.start()

        # Create the main window
        root = tk.Tk()

        #Create tabs
        notebook = ttk.Notebook(root)
        notebook.grid(row=0, column=0, columnspan=2)

        # Tab 1: Lookup
        tab1= ttk.Frame(notebook)
        notebook.add(tab1, text='Lookup')

        uid_label = tk.Label(tab1, text="UID:")
        uid_label.grid(row=0, column=0)
        uid_entry = tk.Entry(tab1)
        uid_entry.grid(row=0, column=1)

        # Tab 2: Add
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text='Add')

        std_id_label = tk.Label(tab2, text="Student ID:")
        std_id_label.grid(row=0, column=0)
        std_id_entry = tk.Entry(tab2)
        std_id_entry.grid(row=0, column=1)

        std_dep_label = tk.Label(tab2, text="Department:")
        std_dep_label.grid(row=1, column=0)
        std_dep_entry = tk.Entry(tab2)
        std_dep_entry.grid(row=1, column=1)

        std_term_label = tk.Label(tab2, text="Term:")
        std_term_label.grid(row=2, column=0)
        std_term_entry = tk.Entry(tab2)
        std_term_entry.grid(row=2, column=1)

        assoc_affil_label = tk.Label(tab2, text="Associate Affiliation:")
        assoc_affil_label.grid(row=3, column=0)
        assoc_affil_var = tk.IntVar()
        assoc_affil_cb = tk.Checkbutton(tab2, variable=assoc_affil_var)
        assoc_affil_cb.grid(row=3, column=1)

        assoc_dep_label = tk.Label(tab2, text="Associate Department:")
        assoc_dep_label.grid(row=4, column=0)
        assoc_dep_entry =tk.Entry(tab2)
        assoc_dep_entry.grid(row=4, column=1)

        assoc_actv_label = tk.Label(tab2, text="Associate Active:")
        assoc_actv_label.grid(row=5, column=0)
        assoc_actv_var = tk.IntVar()
        assoc_actv_cb = tk.Checkbutton(tab2, variable=assoc_actv_var)
        assoc_actv_cb.grid(row=5, column=1)

        assoc_main_accs_label = tk.Label(tab2, text="Main Access:")
        assoc_main_accs_label.grid(row=6, column=0)
        assoc_main_accs_var = tk.IntVar()
        assoc_main_accs_cb = tk.Checkbutton(tab2, variable=assoc_main_accs_var)
        assoc_main_accs_cb.grid(row=6, column=1)

        assoc_office_accs_label = tk.Label(tab2, text="Office Access:")
        assoc_office_accs_label.grid(row=7, column=0)
        assoc_office_accs_var = tk.IntVar()
        assoc_office_accs_cb = tk.Checkbutton(tab2, variable=assoc_office_accs_var)
        assoc_office_accs_cb.grid(row=7, column=1)

        assoc_djroom_accs_label = tk.Label(tab2, text="DJ Room Access:")
        assoc_djroom_accs_label.grid(row=8, column=0)
        assoc_djroom_accs_var = tk.IntVar()
        assoc_djroom_accs_cb = tk.Checkbutton(tab2, variable=assoc_djroom_accs_var)
        assoc_djroom_accs_cb.grid(row=8, column=1)

        first_name_label = tk.Label(tab2, text="First Name:")
        first_name_label.grid(row=9, column=0)
        first_name_entry = tk.Entry(tab2)
        first_name_entry.grid(row=9, column=1)

        last_name_label = tk.Label(tab2, text="Last Name:")
        last_name_label.grid(row=10, column=0)
        last_name_entry = tk.Entry(tab2)
        last_name_entry.grid(row=10, column=1)

        email_label= tk.Label(tab2, text="Email:")
        email_label.grid(row=11, column=0)
        email_entry = tk.Entry(tab2)
        email_entry.grid(row=11, column=1)

        gsm_label = tk.Label(tab2, text="GSM:")
        gsm_label.grid(row=12, column=0)
        gsm_entry = tk.Entry(tab2)
        gsm_entry.grid(row=12, column=1)

        bday_label = tk.Label(tab2, text="Birthday (YYYY-MM-DD):")
        bday_label.grid(row=13, column=0)
        bday_entry = tk.Entry(tab2)
        bday_entry.grid(row=13, column=1)

        submit_button = tk.Button(tab2, text="Submit", command= lambda: submit_form(std_id_entry, std_dep_entry, std_term_entry, assoc_affil_var, assoc_dep_entry, assoc_actv_var, assoc_main_accs_var, assoc_office_accs_var, assoc_djroom_accs_var, first_name_entry, last_name_entry, email_entry, gsm_entry, bday_entry))
        submit_button.grid(row=14, column=0, columnspan=2)

        root.mainloop()
        
if __name__ == "__main__":
    main()