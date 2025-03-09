-- Existing tables
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

-- New tables for enhanced functionality
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(120) UNIQUE NOT NULL,
    username VARCHAR(64) UNIQUE NOT NULL,
    password_hash VARCHAR(128),
    rfid_uid_hash VARCHAR(128) UNIQUE,
    two_factor_secret VARCHAR(32),
    is_active BOOLEAN DEFAULT TRUE,
    role VARCHAR(20) DEFAULT 'member',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    UID INTEGER,
    FOREIGN KEY (UID) REFERENCES School_info(UID),
    INDEX idx_email (email),
    INDEX idx_username (username),
    INDEX idx_rfid (rfid_uid_hash)
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(128) NOT NULL,
    description TEXT,
    start_datetime DATETIME NOT NULL,
    end_datetime DATETIME NOT NULL,
    capacity INTEGER,
    location VARCHAR(256),
    event_type VARCHAR(20),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_start_time (start_datetime),
    INDEX idx_event_type (event_type)
);

CREATE TABLE IF NOT EXISTS event_registrations (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    event_id INTEGER,
    user_id INTEGER,
    registration_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'registered',
    check_in_time DATETIME,
    FOREIGN KEY (event_id) REFERENCES events(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_registration_lookup (event_id, user_id, status)
);

CREATE TABLE IF NOT EXISTS volunteer_shifts (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    event_id INTEGER,
    volunteer_id INTEGER,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    role VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'scheduled',
    priority_score FLOAT DEFAULT 0.0,
    FOREIGN KEY (event_id) REFERENCES events(id),
    FOREIGN KEY (volunteer_id) REFERENCES users(id),
    INDEX idx_shift_scheduling (volunteer_id, start_time, status, priority_score)
);

CREATE TABLE IF NOT EXISTS volunteer_metrics (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    volunteer_id INTEGER UNIQUE,
    total_hours FLOAT DEFAULT 0.0,
    reliability_score FLOAT DEFAULT 1.0,
    seniority_score FLOAT DEFAULT 0.0,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (volunteer_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS access_logs (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER,
    rfid_uid_hash VARCHAR(128),
    success BOOLEAN,
    location VARCHAR(50),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_access_lookup (user_id, timestamp)
);
