from flask import Blueprint, request, jsonify
from datetime import datetime
from database import db
from models.mission import Mission, MissionRecord
from models.daily_mission import DailyMission
from utils.mission_presets import get_mission_presets
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request

missions_bp = Blueprint('missions', __name__)

@missions_bp.route('', methods=['GET'])
def get_all_missions():
    missions = Mission.query.all()
    return jsonify([mission.to_dict() for mission in missions]), 200


@missions_bp.route('/presets', methods=['GET'])
def get_mission_presets_list():
    today = datetime.now().date()
    daily_mission = DailyMission.query.filter_by(date=today).first()

    if not daily_mission:
        return jsonify({'error': '오늘의 미션이 아직 생성되지 않았습니다.'}), 404

    all_presets = daily_mission.to_mission_list()

    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    completed_today = db.session.query(MissionRecord).filter(
        MissionRecord.preset_mission_id.isnot(None),
        MissionRecord.completed_at >= today_start
    ).all()

    completed_ids = {record.preset_mission_id for record in completed_today}

    # 완료되지 않은 미션만 필터링
    available_presets = [m for m in all_presets if m['id'] not in completed_ids]

    return jsonify({'missions': available_presets}), 200

@missions_bp.route('/<int:mission_id>', methods=['GET'])
def get_mission(mission_id):
    mission = Mission.query.get_or_404(mission_id)
    return jsonify(mission.to_dict()), 200

@missions_bp.route('/<int:mission_id>/start', methods=['POST'])
def start_mission(mission_id):
    mission = Mission.query.get_or_404(mission_id)
    return jsonify({
        'mission': mission.to_dict(),
        'started_at': datetime.now().isoformat()
    }), 200

@missions_bp.route('/<int:mission_id>/complete', methods=['POST'])
def complete_mission(mission_id):
    mission = Mission.query.get_or_404(mission_id)
    data = request.get_json() or {}

    record = MissionRecord(
        mission_id=mission_id,
        actual_duration=data.get('actual_duration', mission.duration),
        notes=data.get('notes')
    )

    try:
        db.session.add(record)
        db.session.commit()
        return jsonify(record.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@missions_bp.route('/records', methods=['GET'])
def get_mission_records():
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)

    records = MissionRecord.query\
        .order_by(MissionRecord.completed_at.desc())\
        .limit(limit)\
        .offset(offset)\
        .all()

    total = MissionRecord.query.count()

    return jsonify({
        'records': [record.to_dict() for record in records],
        'total': total,
        'limit': limit,
        'offset': offset
    }), 200

@missions_bp.route('/presets/complete', methods=['POST'])
def complete_preset_mission():
    data = request.get_json()

    if not data or 'preset_mission_id' not in data:
        return jsonify({'error': 'preset_mission_id is required'}), 400

    user_id = None
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        if identity:
            user_id = int(identity)
    except:
        pass

    record = MissionRecord(
        user_id=user_id,
        preset_mission_id=data['preset_mission_id'],
        tier=data.get('tier'),
        title=data.get('title'),
        description=data.get('description'),
        actual_duration=data.get('duration'),
        notes=data.get('notes')
    )

    try:
        db.session.add(record)
        db.session.commit()
        return jsonify(record.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@missions_bp.route('/presets/fail', methods=['POST'])
def fail_preset_mission():
    """미션 실패/취소 기록"""
    data = request.get_json()

    if not data or 'preset_mission_id' not in data:
        return jsonify({'error': 'preset_mission_id is required'}), 400

    user_id = None
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        if identity:
            user_id = int(identity)
    except:
        pass

    record = MissionRecord(
        user_id=user_id,
        preset_mission_id=data['preset_mission_id'],
        tier=data.get('tier'),
        title=data.get('title'),
        description=data.get('description'),
        actual_duration=0,  # 실패는 0으로 표시
        notes='failed'
    )

    try:
        db.session.add(record)
        db.session.commit()
        return jsonify({'message': 'Mission failed recorded', 'record': record.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@missions_bp.route('/medals', methods=['GET'])
def get_earned_medals():
    user_id = None
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        if identity:
            user_id = int(identity)
    except:
        pass

    query = MissionRecord.query.filter(MissionRecord.tier.isnot(None))

    if user_id:
        query = query.filter(MissionRecord.user_id == user_id)

    records = query.all()

    medals = {'bronze': 0, 'silver': 0, 'gold': 0}
    for record in records:
        if record.tier in medals:
            medals[record.tier] += 1

    return jsonify({'medals': medals}), 200


@missions_bp.route('/recent', methods=['GET'])
def get_recent_completed_missions():
    limit = request.args.get('limit', 5, type=int)

    user_id = None
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        if identity:
            user_id = int(identity)
    except:
        pass

    query = MissionRecord.query.filter(MissionRecord.preset_mission_id.isnot(None))

    if user_id:
        query = query.filter(MissionRecord.user_id == user_id)

    records = query.order_by(MissionRecord.completed_at.desc()).limit(limit).all()

    return jsonify({
        'missions': [record.to_dict() for record in records]
    }), 200


@missions_bp.route('', methods=['POST'])
def create_mission():
    data = request.get_json()

    if not data or 'title' not in data or 'duration' not in data:
        return jsonify({'error': 'title and duration are required'}), 400

    mission = Mission(
        title=data['title'],
        description=data.get('description'),
        duration=data['duration'],
        difficulty=data.get('difficulty', 'medium'),
        category=data.get('category')
    )

    try:
        db.session.add(mission)
        db.session.commit()
        return jsonify(mission.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@missions_bp.route('/generate-daily', methods=['POST'])
def generate_daily_missions_manually():
    from services.ai_mission_generator import generate_and_save_daily_missions

    try:
        generate_and_save_daily_missions()
        return jsonify({'message': '오늘의 미션이 성공적으로 생성되었습니다.'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@missions_bp.route('/daily', methods=['GET'])
def get_today_missions():
    today = datetime.now().date()
    daily_mission = DailyMission.query.filter_by(date=today).first()

    if not daily_mission:
        return jsonify({'error': '오늘의 미션이 아직 생성되지 않았습니다.'}), 404

    return jsonify({
        'date': daily_mission.date.isoformat(),
        'missions': daily_mission.to_mission_list()
    }), 200
