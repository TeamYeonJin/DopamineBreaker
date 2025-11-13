from flask import Blueprint, jsonify
from database import db
from models.achievement import Achievement, UserAchievement

achievements_bp = Blueprint('achievements', __name__)

@achievements_bp.route('', methods=['GET'])
def get_all_achievements():
    """모든 업적 조회"""
    achievements = Achievement.query.all()
    return jsonify([achievement.to_dict() for achievement in achievements]), 200

@achievements_bp.route('/<int:achievement_id>', methods=['GET'])
def get_achievement(achievement_id):
    """특정 업적 조회"""
    achievement = Achievement.query.get_or_404(achievement_id)
    return jsonify(achievement.to_dict()), 200

@achievements_bp.route('/user', methods=['GET'])
def get_user_achievements():
    """사용자가 달성한 업적 조회"""
    user_achievements = UserAchievement.query.all()

    # 모든 업적과 사용자 달성 여부 결합
    all_achievements = Achievement.query.all()
    unlocked_ids = {ua.achievement_id for ua in user_achievements}

    result = []
    for achievement in all_achievements:
        achievement_dict = achievement.to_dict()
        achievement_dict['unlocked'] = achievement.id in unlocked_ids
        if achievement.id in unlocked_ids:
            user_achievement = next(ua for ua in user_achievements if ua.achievement_id == achievement.id)
            achievement_dict['unlocked_at'] = user_achievement.unlocked_at.isoformat()
        result.append(achievement_dict)

    return jsonify(result), 200

@achievements_bp.route('/<int:achievement_id>/unlock', methods=['POST'])
def unlock_achievement(achievement_id):
    """업적 달성"""
    achievement = Achievement.query.get_or_404(achievement_id)

    # 이미 달성했는지 확인
    existing = UserAchievement.query.filter_by(achievement_id=achievement_id).first()
    if existing:
        return jsonify({'message': 'Achievement already unlocked', 'achievement': existing.to_dict()}), 200

    user_achievement = UserAchievement(achievement_id=achievement_id)

    try:
        db.session.add(user_achievement)
        db.session.commit()
        return jsonify(user_achievement.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500