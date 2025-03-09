#!/usr/bin/env python3
import os
import sys
import subprocess
import secrets
import mysql.connector
from dotenv import load_dotenv

def generate_secret_key():
    """Generate a secure secret key"""
    return secrets.token_hex(32)

def update_env_file():
    """Update environment variables with secure values"""
    env_updates = {
        'SECRET_KEY': generate_secret_key(),
        'SECURITY_PASSWORD_SALT': generate_secret_key(),
        'RFID_HASH_SALT': generate_secret_key()
    }
    
    with open('.env', 'r') as f:
        lines = f.readlines()
    
    updated_lines = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            key = line.split('=')[0]
            if key in env_updates:
                line = f"{key}={env_updates[key]}"
                env_updates.pop(key)
        updated_lines.append(line)
    
    # Add any remaining new variables
    for key, value in env_updates.items():
        updated_lines.append(f"{key}={value}")
    
    with open('.env', 'w') as f:
        f.write('\n'.join(updated_lines))

def setup_database():
    """Initialize database and create required tables"""
    load_dotenv()
    
    # Database connection parameters
    db_params = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD'),
    }
    
    try:
        # Connect to MySQL server
        conn = mysql.connector.connect(**db_params)
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        db_name = os.getenv('DB_NAME', 'rht_rfid')
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.execute(f"USE {db_name}")
        
        # Create tables
        with open('schema.sql', 'r') as f:
            sql_commands = f.read().split(';')
            for command in sql_commands:
                if command.strip():
                    cursor.execute(command)
        
        conn.commit()
        print("Database setup completed successfully")
        
    except mysql.connector.Error as err:
        print(f"Error setting up database: {err}")
        sys.exit(1)
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def setup_virtual_environment():
    """Set up Python virtual environment and install dependencies"""
    try:
        # Create virtual environment
        if not os.path.exists('venv'):
            subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
        
        # Determine the pip path based on OS
        if sys.platform == 'win32':
            pip_path = os.path.join('venv', 'Scripts', 'pip')
        else:
            pip_path = os.path.join('venv', 'bin', 'pip')
        
        # Install dependencies
        subprocess.run([pip_path, 'install', '-e', '.'], check=True)
        print("Virtual environment setup completed successfully")
        
    except subprocess.CalledProcessError as e:
        print(f"Error setting up virtual environment: {e}")
        sys.exit(1)

def create_directories():
    """Create necessary directories for the application"""
    directories = [
        'logs',
        'static/qrcodes',
        'instance',
        'migrations'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def main():
    """Main setup function"""
    print("Starting RHT RFID system setup...")
    
    # Check if running from correct directory
    if not os.path.exists('setup.py'):
        print("Error: Please run this script from the project root directory")
        sys.exit(1)
    
    # Create necessary directories
    print("Creating directory structure...")
    create_directories()
    
    # Update environment variables
    print("Updating environment variables...")
    update_env_file()
    
    # Set up virtual environment
    print("Setting up virtual environment...")
    setup_virtual_environment()
    
    # Set up database
    print("Setting up database...")
    setup_database()
    
    print("\nSetup completed successfully!")
    print("\nNext steps:")
    print("1. Activate the virtual environment:")
    print("   - On Windows: .\\venv\\Scripts\\activate")
    print("   - On Unix/MacOS: source venv/bin/activate")
    print("2. Update the .env file with your specific configuration")
    print("3. Start the development server: flask run")

if __name__ == '__main__':
    main()
