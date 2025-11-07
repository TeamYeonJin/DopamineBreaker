from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from models.mission import Mission, MissionRecord
from utils.mission_presets import get_mission_presets

missions_bp = Blueprint('missions', __name__)

@missions_bp.route('', methods=['GET'])
def get_all_missions():
    """모든 미션 조회"""
    missions = Mission.query.all()
    return jsonify([mission.to_dict() for mission in missions]), 200


@missions_bp.route('/presets', methods=['GET'])
def get_mission_presets_list():
    """설정 파일에 정의된 미션 프리셋 조회"""
    return jsonify({'missions': get_mission_presets()}), 200

@missions_bp.route('/<int:mission_id>', methods=['GET'])
def get_mission(mission_id):
    """특정 미션 조회"""
    mission = Mission.query.get_or_404(mission_id)
    return jsonify(mission.to_dict()), 200

@missions_bp.route('/<int:mission_id>/start', methods=['POST'])
def start_mission(mission_id):
    """미션 시작"""
    mission = Mission.query.get_or_404(mission_id)
    return jsonify({
        'mission': mission.to_dict(),
        'started_at': datetime.now().isoformat()
    }), 200

@missions_bp.route('/<int:mission_id>/complete', methods=['POST'])
def complete_mission(mission_id):
    """미션 완료"""
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
    """완료한 미션 기록 조회"""
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

@missions_bp.route('', methods=['POST'])
def create_mission():
    """새 미션 생성 (관리자용)"""
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
