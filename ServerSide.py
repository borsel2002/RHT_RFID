import mysql.connector
import os
import serial
import time
from dotenv import load_dotenv

# Load environment variables
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
        database=os.getenv('DB_NAME')  
    )
    c = conn.cursor()

    # Check if the UID has access
    c.execute("SELECT Assoc_Accs_1, Assoc_Accs_2, Assoc_Accs_3 FROM Assoc_info WHERE UID = %s", (uid,))
    row = c.fetchone()
    conn.close()
    
    if row:
        access_index = {'Ana Kapı': 0, 'Yayın Odası': 1, 'DJ Odası': 2}
        if row[access_index[doorName]]:
            return '1'  # Access granted
    return '0'  # Access denied

# Function to insert information into the database
def insert_into_database(uid, std_dep, std_term, assoc_info, personal_info):
    # Connect to the MySQL database
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
    c.execute("INSERT INTO Assoc_info (UID, Assoc_Affil, Assoc_Dep, Assoc_Actv, Assoc_Accs_1, Assoc_Accs_2, Assoc_Accs_3) VALUES (%s, %s, %s, %s, %s, %s, %s)", (uid, *assoc_info))
    # Insert into Personal_info
    c.execute("INSERT INTO Personal_info (UID, FirstName, LastName, eMail, GSM, BDay) VALUES (%s, %s, %s, %s, %s, %s)", (uid, *personal_info))

    conn.commit()
    conn.close()

# CLI for adding information
def cli_add_info():
    uid = input("Enter UID: ")
    std_dep = input("Enter Student Department: ")
    std_term = input("Enter Student Term: ")
    assoc_info = [
        input("Enter Assoc Affiliation (True/False): "),
        input("Enter Assoc Department: "),
        input("Enter Assoc Active (True/False): "),
        input("Enter Access 1 (True/False): "),
        input("Enter Access 2 (True/False): "),
        input("Enter Access 3 (True/False): ")
    ]
    personal_info = [
        input("Enter First Name: "),
        input("Enter Last Name: "),
        input("Enter Email: "),
        input("Enter GSM: "),
        input("Enter Birth Date (YYYY-MM-DD): ")
    ]
    insert_into_database(uid, std_dep, std_term, assoc_info, personal_info)
    print("Information added to the database.")

# Main loop to listen for UIDs from the Arduino
while True:
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').strip().split(',')
        uid, doorName = data[0], data[1]  # Parse UID and door name from serial
        if doorName == "Ana Kapı" and uid == "command":  # Check for the special command to activate CLI
            cli_add_info()
        else:
            print(f'Received UID: {uid} for {doorName}')
            response = check_uid_in_database(uid, doorName)  # Check the UID against the database
            ser.write(response.encode())  # Send the response back to the Arduino
            print(f'Sent response: {response}')
            
