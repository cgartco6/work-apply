from app import db
from datetime import datetime
import uuid
import json

class JobApplication(db.Model):
    __tablename__ = 'job_applications'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    original_resume = db.Column(db.Text, nullable=False)
    enhanced_resume = db.Column(db.Text)
    cover_letter = db.Column(db.Text)
    target_region = db.Column(db.String(100), nullable=False)
    target_town = db.Column(db.String(100))
    job_title = db.Column(db.String(200))
    industry = db.Column(db.String(100))
    status = db.Column(db.String(50), default='pending')  # pending, processing, completed, failed
    applications_sent = db.Column(db.Integer, default=0)
    matches_found = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Store job matches as JSON
    job_matches = db.Column(db.Text)
    
    def set_job_matches(self, matches):
        self.job_matches = json.dumps(matches)
    
    def get_job_matches(self):
        return json.loads(self.job_matches) if self.job_matches else []
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'target_region': self.target_region,
            'target_town': self.target_town,
            'job_title': self.job_title,
            'industry': self.industry,
            'status': self.status,
            'applications_sent': self.applications_sent,
            'matches_found': self.matches_found,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'job_matches': self.get_job_matches()
        }
