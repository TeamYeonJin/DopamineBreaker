from flask import Blueprint, request, jsonify
from datetime import datetime, date
from database import db
from models.screen_time import ScreenTime

screen_time_bp = Blueprint('screen_time', __name__)

@screen_time_bp.route('/today', methods=['GET'])
def get_today_screen_time():
    today = date.today()
    records = ScreenTime.query.filter_by(date=today).all()

    total_time = sum(record.usage_time for record in records)
    apps = [record.to_dict() for record in records]

    return jsonify({
        'date': today.isoformat(),
        'total': total_time,
        'apps': apps
    }), 200

@screen_time_bp.route('/range', methods=['GET'])
def get_screen_time_by_range():
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')

    if not start_date or not end_date:
        return jsonify({'error': 'startDate and endDate are required'}), 400

    try:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    records = ScreenTime.query.filter(
        ScreenTime.date >= start,
        ScreenTime.date <= end
    ).all()

    return jsonify({
        'start_date': start.isoformat(),
        'end_date': end.isoformat(),
        'records': [record.to_dict() for record in records]
    }), 200

@screen_time_bp.route('', methods=['POST'])
def record_screen_time():
    data = request.get_json()

    if not data or 'app_name' not in data or 'usage_time' not in data:
        return jsonify({'error': 'app_name and usage_time are required'}), 400

    record_date = datetime.strptime(data.get('date', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d').date()

    screen_time = ScreenTime(
        date=record_date,
        app_name=data['app_name'],
        category=data.get('category'),
        usage_time=data['usage_time']
    )

    try:
        db.session.add(screen_time)
        db.session.commit()
        return jsonify(screen_time.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
