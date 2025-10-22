from app import db
from datetime import datetime
import uuid

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), default='ZAR')
    payment_method = db.Column(db.String(50), nullable=False)  # payfast, eft
    status = db.Column(db.String(50), default='pending')  # pending, completed, failed, cancelled
    payfast_payment_id = db.Column(db.String(100))
    merchant_id = db.Column(db.String(100))
    eft_reference = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': float(self.amount),
            'currency': self.currency,
            'payment_method': self.payment_method,
            'status': self.status,
            'eft_reference': self.eft_reference,
            'created_at': self.created_at.isoformat()
        }
