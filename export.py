import mysql.connector
import csv
from dotenv import load_dotenv
import os
load_dotenv()
conn = mysql.connector.connect(
    host=os.getenv('DB_HOST'), 
    user=os.getenv('DB_USER'), 
    password=os.getenv('DB_PASSWORD'),  
    database=os.getenv('DB_NAME')  
)
c = conn.cursor()
c.execute('''
    SELECT 
        Assoc_info.UID,
        Assoc_main_Accs,
        Assoc_office_Accs,
        Assoc_djroom_Accs
    FROM 
        Assoc_info
    INNER JOIN 
        School_info ON Assoc_info.UID = School_info.UID
''')
rows = c.fetchall()
with open('access_db.txt', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)
conn.close()
