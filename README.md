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
    UID INTEGER,
    FOREIGN KEY (UID) REFERENCES School_info(UID)
);

CREATE TABLE IF NOT EXISTS Personal_info (
    P_ID INTEGER AUTO_INCREMENT PRIMARY KEY,
    FirstName TEXT,
    LastName TEXT,
    eMail TEXT,
    GSM INTEGER,
    BDay DATE,
    UID INTEGER,
    FOREIGN KEY (UID) REFERENCES School_info(UID)
);

