# Simple RFID Membership System

## Overview
A streamlined membership and event management system designed for student associations, using RFID technology for member identification and event check-ins. This system focuses on membership management, event organization, and volunteer coordination.

## Features

### 1. Membership Management
- Student information tracking
- Association affiliations
- Membership status and validity periods
- Automated membership expiration handling
- RFID-based member identification

### 2. Event Management
- Event creation and scheduling
- Ticket registration system
- RFID-based attendance tracking
- Capacity management
- Real-time availability updates

### 3. Volunteer System
- AI-driven scheduling system
- Volunteer shift management
- Performance metrics tracking
- Automated volunteer assignment
- Seniority-based priority system

## Hardware Requirements

### 1. RFID Components
- MFRC522 RFID reader module
- Compatible RFID cards/tags (13.56 MHz)
- Arduino/ESP8266/ESP32 microcontroller
- USB connection cables
- Power supply (5V)

### 2. Server Requirements
- Web server (Apache/Nginx)
- MySQL database server
- Redis server for caching
- Basic network infrastructure

## Software Stack

### 1. Backend (Python/Flask)
- RESTful API endpoints
- SQLAlchemy ORM
- Redis caching
- Basic authentication
- Rate limiting

### 2. Frontend
- Web interface for administrators
- Mobile-responsive design
- Real-time updates
- Member/Event management dashboard

### 3. Arduino Software
- RFID reading functionality
- Serial communication with server
- Basic error handling

## Security Features

1. **Authentication**
   - Password hashing with bcrypt
   - Session management
   - Role-based access control

2. **System Security**
   - Rate limiting on endpoints
   - Request tracking and logging
   - SQL injection prevention
   - CSRF protection

## Setup Instructions

1. **Environment Setup**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

2. **Database Setup**
```bash
# Initialize database
flask db init
flask db migrate
flask db upgrade
```

3. **Create Admin User**
```bash
# Create initial admin user
flask rht create-admin
```

4. **Run Development Server**
```bash
flask run
```

## API Endpoints

### Authentication
- POST `/auth/login` - User login
- POST `/auth/logout` - User logout

### Members
- GET `/api/members` - List members
- POST `/api/members` - Create member
- GET `/api/members/<id>` - Get member details
- PUT `/api/members/<id>` - Update member
- DELETE `/api/members/<id>` - Delete member

### Events
- GET `/api/events` - List events
- POST `/api/events` - Create event
- GET `/api/events/<id>` - Get event details
- PUT `/api/events/<id>` - Update event
- DELETE `/api/events/<id>` - Delete event
- POST `/api/events/<id>/register` - Register for event
- POST `/api/events/<id>/check-in` - Check-in to event

### Volunteers
- GET `/api/volunteers` - List volunteers
- POST `/api/volunteers` - Create volunteer
- GET `/api/shifts` - List shifts
- POST `/api/shifts` - Create shift
- PUT `/api/shifts/<id>` - Update shift

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details
