from datetime import datetime
from database import db

class Mission(db.Model):
    """미션 모델"""
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    duration = db.Column(db.Integer, nullable=False)  # 분 단위
    difficulty = db.Column(db.String(20))  # easy, medium, hard
    category = db.Column(db.String(50))  # physical, mental, health
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # MissionRecord와의 관계
    records = db.relationship('MissionRecord', backref='mission', lazy=True)

    def __repr__(self):
        return f'<Mission {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'duration': self.duration,
            'difficulty': self.difficulty,
            'category': self.category,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class MissionRecord(db.Model):
    """미션 완료 기록 모델"""
    __tablename__ = 'mission_records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    mission_id = db.Column(db.Integer, db.ForeignKey('missions.id'), nullable=True)
    preset_mission_id = db.Column(db.Integer, nullable=True)  # AI 생성 미션 ID
    tier = db.Column(db.String(20), nullable=True)  # bronze, silver, gold
    title = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    actual_duration = db.Column(db.Integer)  # 실제 소요 시간 (분)
    notes = db.Column(db.Text)

    def __repr__(self):
        return f'<MissionRecord mission_id={self.mission_id} completed_at={self.completed_at}>'

    def to_dict(self):
        return {
            'id': self.id,
            'mission_id': self.mission_id,
            'preset_mission_id': self.preset_mission_id,
            'tier': self.tier,
            'title': self.title,
            'description': self.description,
            'mission': self.mission.to_dict() if self.mission else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'actual_duration': self.actual_duration,
            'notes': self.notes
        }
