import hashlib
import qrcode
import os
from datetime import datetime
from flask import current_app
from app.models import User, db
from app import cache

class RFIDManager:
    def __init__(self, salt=None):
        self.salt = salt or current_app.config['RFID_HASH_SALT']
        self.qr_path = current_app.config['QRCODE_DIR']
        
        # Ensure QR code directory exists
        if not os.path.exists(self.qr_path):
            os.makedirs(self.qr_path)
    
    def hash_uid(self, uid):
        """Generate secure hash of RFID UID"""
        return hashlib.sha256(f"{uid}{self.salt}".encode()).hexdigest()
    
    @cache.memoize(timeout=300)
    def verify_uid(self, uid, stored_hash):
        """Verify RFID UID against stored hash"""
        return self.hash_uid(uid) == stored_hash
    
    def register_rfid(self, user_id, rfid_uid):
        """Register RFID card to user"""
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
            
        # Check if RFID is already registered
        existing_user = User.query.filter_by(
            rfid_uid_hash=self.hash_uid(rfid_uid)
        ).first()
        
        if existing_user and existing_user.id != user_id:
            raise ValueError("RFID card already registered to another user")
            
        user.rfid_uid_hash = self.hash_uid(rfid_uid)
        db.session.commit()
        
        # Generate QR code for backup access
        self.generate_backup_qr(user)
        return True
    
    def generate_backup_qr(self, user):
        """Generate QR code for backup authentication"""
        # Generate temporary token
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M')
        token = hashlib.sha256(
            f"{user.id}{user.email}{timestamp}{self.salt}".encode()
        ).hexdigest()
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # Add data
        qr.add_data({
            'user_id': user.id,
            'email': user.email,
            'token': token,
            'timestamp': timestamp
        })
        qr.make(fit=True)
        
        # Save QR code
        img = qr.make_image(fill_color="black", back_color="white")
        qr_filename = f"backup_qr_{user.id}_{timestamp}.png"
        img.save(os.path.join(self.qr_path, qr_filename))
        
        return qr_filename
    
    @cache.memoize(timeout=300)
    def verify_backup_qr(self, qr_data):
        """Verify backup QR code data"""
        try:
            user = User.query.get(qr_data['user_id'])
            if not user or user.email != qr_data['email']:
                return False
                
            # Verify token
            timestamp = datetime.strptime(qr_data['timestamp'], '%Y%m%d%H%M')
            expected_token = hashlib.sha256(
                f"{user.id}{user.email}{qr_data['timestamp']}{self.salt}".encode()
            ).hexdigest()
            
            # Check if token matches and is not expired (24 hours validity)
            if (qr_data['token'] != expected_token or
                (datetime.utcnow() - timestamp).total_seconds() > 86400):
                return False
                
            return user
            
        except (KeyError, ValueError):
            return False
    
    def deactivate_rfid(self, user_id):
        """Deactivate RFID access for user"""
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
            
        user.rfid_uid_hash = None
        db.session.commit()
        return True
    
    def get_access_logs(self, user_id, days=30):
        """Get RFID access logs for user"""
        from app.models import AccessLog
        
        return AccessLog.query.filter(
            AccessLog.user_id == user_id,
            AccessLog.timestamp >= datetime.utcnow() - timedelta(days=days)
        ).order_by(AccessLog.timestamp.desc()).all()
    
    def log_access_attempt(self, rfid_uid, success, location=None):
        """Log RFID access attempt"""
        from app.models import AccessLog
        
        user = User.query.filter_by(rfid_uid_hash=self.hash_uid(rfid_uid)).first()
        log = AccessLog(
            user_id=user.id if user else None,
            rfid_uid_hash=self.hash_uid(rfid_uid),
            success=success,
            location=location,
            timestamp=datetime.utcnow()
        )
        
        db.session.add(log)
        db.session.commit()
        return log
