CREATE TABLE IF NOT EXISTS School_info (
    Std_ID INTEGER PRIMARY KEY,
    Std_Dep TEXT,
    Std_Term INTEGER,
    UID INTEGER UNIQUE
);

CREATE TABLE IF NOT EXISTS Assoc_info (
    Assoc_ID INTEGER AUTO_INCREMENT PRIMARY KEY,
    Assoc_Affil BOOLEAN,
    Assoc_Dep TEXT,
    Assoc_Actv BOOLEAN,
    Assoc_main_Accs BOOLEAN,
    Assoc_office_Accs BOOLEAN,
    Assoc_djroom_Accs BOOLEAN,
    Std_ID INTEGER,
    FOREIGN KEY (Std_ID) REFERENCES School_info(Std_ID)
);

CREATE TABLE IF NOT EXISTS Personal_info (
    P_ID INTEGER AUTO_INCREMENT PRIMARY KEY,
    FirstName TEXT,
    LastName TEXT,
    eMail TEXT,
    GSM INTEGER,
    BDay DATE,
    Std_ID INTEGER,
    FOREIGN KEY (Std_ID) REFERENCES School_info(Std_ID)
);



+--------------------+
| Tables_in_rht_rfid |
+--------------------+
| Assoc_info         |
| Personal_info      |
| School_info        |
+--------------------+





+-------------------+------------+------+-----+---------+----------------+
| Field             | Type       | Null | Key | Default | Extra          |
+-------------------+------------+------+-----+---------+----------------+
| Assoc_ID          | int(11)    | NO   | PRI | NULL    | auto_increment |
| Assoc_Affil       | tinyint(1) | YES  |     | NULL    |                |
| Assoc_Dep         | text       | YES  |     | NULL    |                |
| Assoc_Actv        | tinyint(1) | YES  |     | NULL    |                |
| Assoc_main_Accs   | tinyint(1) | YES  |     | NULL    |                |
| Assoc_office_Accs | tinyint(1) | YES  |     | NULL    |                |
| Assoc_djroom_Accs | tinyint(1) | YES  |     | NULL    |                |
| Std_ID            | int(11)    | YES  | MUL | NULL    |                |
+-------------------+------------+------+-----+---------+----------------+




+-----------+---------+------+-----+---------+----------------+
| Field     | Type    | Null | Key | Default | Extra          |
+-----------+---------+------+-----+---------+----------------+
| P_ID      | int(11) | NO   | PRI | NULL    | auto_increment |
| FirstName | text    | YES  |     | NULL    |                |
| LastName  | text    | YES  |     | NULL    |                |
| eMail     | text    | YES  |     | NULL    |                |
| GSM       | int(11) | YES  |     | NULL    |                |
| BDay      | date    | YES  |     | NULL    |                |
| Std_ID    | int(11) | YES  | MUL | NULL    |                |
+-----------+---------+------+-----+---------+----------------+




+----------+---------+------+-----+---------+-------+
| Field    | Type    | Null | Key | Default | Extra |
+----------+---------+------+-----+---------+-------+
| Std_ID   | int(11) | NO   | PRI | NULL    |       |
| Std_Dep  | text    | YES  |     | NULL    |       |
| Std_Term | int(11) | YES  |     | NULL    |       |
| UID      | int(11) | YES  | UNI | NULL    |       |
+----------+---------+------+-----+---------+-------+
