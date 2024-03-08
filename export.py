import mysql.connector
import os
import serial
import time
from dotenv import load_dotenv

load_dotenv()

ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

def check_uid_in_database(uid, doorName):
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'), 
        user=os.getenv('DB_USER'), 
        password=os.getenv('DB_PASSWORD'),  
        database=os.getenv('DB_NAME')  
    )
    c = conn.cursor()

    query = '''
        SELECT 
            Assoc_info.UID,
            Assoc_main_Accs,
            Assoc_office_Accs,
            Assoc_djroom_Accs
        FROM 
            Assoc_info
        INNER JOIN 
            School_info ON Assoc_info.UID = School_info.UID
        WHERE
            Assoc_info.UID = %s
    '''
    c.execute(query, (uid,))
    row = c.fetchone()
    conn.close()

    if row:
        access_index = {'Ana Kapı': 1, 'Yayın Odası': 2, 'DJ Odası': 3}
        if row[access_index[doorName]]:
            return '1'
    return '0'

while True:
    if ser.in_waiting > 0:
        uid = ser.readline().decode('utf-8').strip()
        doorName = ser.readline().decode('utf-8').strip()
        print(f'Received UID: {uid} for {doorName}')
        response = check_uid_in_database(uid, doorName)
        ser.write(response.encode())
        print(f'Sent response: {response}')
