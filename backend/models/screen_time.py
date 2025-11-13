from datetime import datetime
from database import db

class ScreenTime(db.Model):
    __tablename__ = 'screen_time'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, index=True)
    app_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))  # social, entertainment, productivity, health
    usage_time = db.Column(db.Integer, nullable=False)  # 분 단위
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ScreenTime {self.app_name} - {self.date}>'

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date else None,
            'app_name': self.app_name,
            'category': self.category,
            'usage_time': self.usage_time,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
