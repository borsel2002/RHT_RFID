# RHT RFID System Versions

This repository contains two main versions of the RHT RFID System, each designed for different use cases:

## Full Version (main branch)

### Features
1. **Access Control**
   - Door access management
   - RFID UID hashing with salt
   - Two-factor authentication
   - QR code backup system
   - Access logs and monitoring

2. **Security Features**
   - Encrypted RFID communication
   - Two-factor authentication with TOTP
   - Advanced session management
   - Access level control (main, office, DJ room)
   - Security event logging

3. **Core Features**
   - Membership management
   - Event registration
   - Volunteer scheduling
   - Attendance tracking
   - Performance metrics

### Hardware Requirements
- MFRC522 RFID reader
- Electronic door locks
- Relay modules
- Power supply units
- Backup batteries
- Network infrastructure

### Setup Instructions
1. **Hardware Setup**
   ```bash
   # Clone the repository
   git clone https://github.com/borsel2002/RHT_RFID.git
   git checkout main
   
   # Install Arduino IDE and required libraries
   # Upload rfid/rfid.ino to your Arduino
   ```

2. **Software Setup**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Configure environment
   cp .env.example .env
   # Edit .env with your settings including RFID_SALT and 2FA configs
   ```

3. **Database Setup**
   ```bash
   # Initialize database
   flask db init
   flask db migrate
   flask db upgrade
   
   # Create admin user
   flask rht create-admin
   ```

## Simple Version (simple_membership branch)

### Features
1. **Member Management**
   - Basic RFID identification
   - Membership tracking
   - Simple authentication
   - Member profiles

2. **Event System**
   - Event creation
   - Registration management
   - Attendance tracking
   - Capacity control

3. **Volunteer Management**
   - Shift scheduling
   - Performance tracking
   - Automated assignments
   - Seniority system

### Hardware Requirements
- MFRC522 RFID reader
- Arduino/ESP8266/ESP32
- USB connection cables
- Basic power supply

### Setup Instructions
1. **Hardware Setup**
   ```bash
   # Clone the repository
   git clone https://github.com/borsel2002/RHT_RFID.git
   git checkout simple_membership
   
   # Upload rfid/rfid.ino to your Arduino
   ```

2. **Software Setup**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Configure environment
   cp .env.example .env
   # Edit .env with basic settings (no security keys needed)
   ```

3. **Database Setup**
   ```bash
   # Initialize database
   flask db init
   flask db migrate
   flask db upgrade
   
   # Create admin user
   flask rht create-admin
   ```

## Switching Between Versions

### To Use Full Version
```bash
git checkout main
pip install -r requirements.txt
flask db upgrade
```

### To Use Simple Version
```bash
git checkout simple_membership
pip install -r requirements.txt
flask db upgrade
```

## Migration Between Versions

### From Full to Simple
1. Backup your database
2. Switch to simple_membership branch
3. Run migrations:
   ```bash
   flask db upgrade
   ```
   This will automatically:
   - Remove door access tables
   - Simplify RFID storage
   - Remove 2FA data
   - Preserve core member data

### From Simple to Full
1. Backup your database
2. Switch to main branch
3. Run migrations:
   ```bash
   flask db upgrade
   ```
4. Additional setup needed:
   - Generate RFID salts
   - Set up 2FA for users
   - Configure door access levels

## API Differences

### Full Version Additional Endpoints
- `/api/access/door` - Door access control
- `/api/auth/2fa` - 2FA management
- `/api/access/logs` - Access logging
- `/api/security/*` - Security endpoints

### Simple Version Endpoints
- `/api/members/*` - Member management
- `/api/events/*` - Event management
- `/api/volunteers/*` - Volunteer management

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support
For issues and feature requests, please use the GitHub issue tracker.
