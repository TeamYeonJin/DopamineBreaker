from flask import Blueprint, jsonify
from datetime import datetime, timedelta, date
from sqlalchemy import func
from database import db
from models.screen_time import ScreenTime
from models.mission import MissionRecord

statistics_bp = Blueprint('statistics', __name__)

@statistics_bp.route('/weekly', methods=['GET'])
def get_weekly_statistics():
    today = date.today()
    week_ago = today - timedelta(days=7)

    screen_time_data = db.session.query(
        ScreenTime.date,
        func.sum(ScreenTime.usage_time).label('total_time')
    ).filter(
        ScreenTime.date >= week_ago,
        ScreenTime.date <= today
    ).group_by(ScreenTime.date).all()

    detox_data = db.session.query(
        func.date(MissionRecord.completed_at).label('date'),
        func.sum(MissionRecord.actual_duration).label('total_time')
    ).filter(
        func.date(MissionRecord.completed_at) >= week_ago,
        func.date(MissionRecord.completed_at) <= today
    ).group_by(func.date(MissionRecord.completed_at)).all()

    screen_time_dict = {str(record.date): record.total_time for record in screen_time_data}
    detox_dict = {str(record.date): record.total_time for record in detox_data}

    weekly_data = []
    for i in range(7):
        day = today - timedelta(days=6-i)
        day_str = str(day)
        weekly_data.append({
            'date': day_str,
            'day': day.strftime('%a'),
            'screenTime': screen_time_dict.get(day_str, 0),
            'detoxTime': detox_dict.get(day_str, 0)
        })

    return jsonify(weekly_data), 200

@statistics_bp.route('/monthly', methods=['GET'])
def get_monthly_statistics():
    today = date.today()
    month_ago = today - timedelta(days=30)

    total_screen_time = db.session.query(
        func.sum(ScreenTime.usage_time)
    ).filter(
        ScreenTime.date >= month_ago,
        ScreenTime.date <= today
    ).scalar() or 0

    total_missions = MissionRecord.query.filter(
        func.date(MissionRecord.completed_at) >= month_ago,
        func.date(MissionRecord.completed_at) <= today
    ).count()

    total_detox_time = db.session.query(
        func.sum(MissionRecord.actual_duration)
    ).filter(
        func.date(MissionRecord.completed_at) >= month_ago,
        func.date(MissionRecord.completed_at) <= today
    ).scalar() or 0

    return jsonify({
        'period': 'monthly',
        'total_screen_time': total_screen_time,
        'total_missions': total_missions,
        'total_detox_time': total_detox_time
    }), 200

@statistics_bp.route('/overall', methods=['GET'])
def get_overall_statistics():
    total_missions = MissionRecord.query.count()
    total_detox_time = db.session.query(
        func.sum(MissionRecord.actual_duration)
    ).scalar() or 0
    records = db.session.query(
        func.date(MissionRecord.completed_at).label('date')
    ).group_by(func.date(MissionRecord.completed_at)).order_by(
        func.date(MissionRecord.completed_at).desc()
    ).all()

    current_streak = 0
    longest_streak = 0
    temp_streak = 0

    if records:
        prev_date = None
        for record in records:
            if prev_date is None:
                temp_streak = 1
            elif (prev_date - record.date).days == 1:
                temp_streak += 1
            else:
                if prev_date == date.today() or (date.today() - prev_date).days == 1:
                    current_streak = temp_streak
                longest_streak = max(longest_streak, temp_streak)
                temp_streak = 1

            prev_date = record.date

        longest_streak = max(longest_streak, temp_streak)
        if prev_date == date.today() or (date.today() - prev_date).days == 1:
            current_streak = temp_streak

    return jsonify({
        'total_missions': total_missions,
        'total_detox_time': total_detox_time,
        'current_streak': current_streak,
        'longest_streak': longest_streak
    }), 200
