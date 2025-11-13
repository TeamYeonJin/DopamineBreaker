from app import create_app
from database import db
from models.mission import MissionRecord
from datetime import datetime, timedelta

def add_sample_missions():
    """샘플 미션 완료 기록 추가"""
    app = create_app()

    with app.app_context():
        # 기존 데이터 확인
        existing_count = MissionRecord.query.count()
        if existing_count > 0:
            print(f"이미 {existing_count}개의 미션 기록이 있습니다.")
            response = input("기존 데이터를 삭제하고 새로 추가하시겠습니까? (y/n): ")
            if response.lower() == 'y':
                MissionRecord.query.delete()
                db.session.commit()
                print("기존 데이터를 삭제했습니다.")
            else:
                print("데이터 추가를 취소합니다.")
                return

        # 샘플 미션 데이터
        sample_missions = [
            {
                'preset_mission_id': 1,
                'tier': 'bronze',
                'title': '목과 어깨 스트레칭',
                'description': '간단한 목과 어깨 스트레칭으로 긴장을 풀어보세요',
                'actual_duration': 5,
                'completed_at': datetime.now() - timedelta(hours=2)
            },
            {
                'preset_mission_id': 2,
                'tier': 'bronze',
                'title': '깊은 호흡',
                'description': '깊은 호흡으로 마음을 안정시켜보세요',
                'actual_duration': 10,
                'completed_at': datetime.now() - timedelta(hours=5)
            },
            {
                'preset_mission_id': 3,
                'tier': 'bronze',
                'title': '수분 보충',
                'description': '물 한 잔을 천천히 마시며 수분을 보충하세요',
                'actual_duration': 3,
                'completed_at': datetime.now() - timedelta(days=1, hours=3)
            },
            {
                'preset_mission_id': 4,
                'tier': 'silver',
                'title': '독서 휴식',
                'description': '좋아하는 책을 읽으며 휴식을 취해보세요',
                'actual_duration': 20,
                'completed_at': datetime.now() - timedelta(days=1, hours=8)
            },
            {
                'preset_mission_id': 5,
                'tier': 'silver',
                'title': '짧은 산책',
                'description': '밖에 나가서 짧은 산책을 즐겨보세요',
                'actual_duration': 15,
                'completed_at': datetime.now() - timedelta(days=2, hours=5)
            },
            {
                'preset_mission_id': 1,
                'tier': 'bronze',
                'title': '목과 어깨 스트레칭',
                'description': '간단한 목과 어깨 스트레칭으로 긴장을 풀어보세요',
                'actual_duration': 5,
                'completed_at': datetime.now() - timedelta(days=3)
            },
            {
                'preset_mission_id': 2,
                'tier': 'bronze',
                'title': '깊은 호흡',
                'description': '깊은 호흡으로 마음을 안정시켜보세요',
                'actual_duration': 10,
                'completed_at': datetime.now() - timedelta(days=3, hours=6)
            },
            {
                'preset_mission_id': 4,
                'tier': 'silver',
                'title': '독서 휴식',
                'description': '좋아하는 책을 읽으며 휴식을 취해보세요',
                'actual_duration': 20,
                'completed_at': datetime.now() - timedelta(days=4, hours=2)
            },
            {
                'preset_mission_id': 1,
                'tier': 'bronze',
                'title': '목과 어깨 스트레칭',
                'description': '간단한 목과 어깨 스트레칭으로 긴장을 풀어보세요',
                'actual_duration': 5,
                'completed_at': datetime.now() - timedelta(days=5)
            },
            {
                'preset_mission_id': 2,
                'tier': 'bronze',
                'title': '깊은 호흡',
                'description': '깊은 호흡으로 마음을 안정시켜보세요',
                'actual_duration': 10,
                'completed_at': datetime.now() - timedelta(days=5, hours=4)
            },
            {
                'preset_mission_id': 5,
                'tier': 'silver',
                'title': '짧은 산책',
                'description': '밖에 나가서 짧은 산책을 즐겨보세요',
                'actual_duration': 15,
                'completed_at': datetime.now() - timedelta(days=6)
            },
            {
                'preset_mission_id': 3,
                'tier': 'bronze',
                'title': '수분 보충',
                'description': '물 한 잔을 천천히 마시며 수분을 보충하세요',
                'actual_duration': 3,
                'completed_at': datetime.now() - timedelta(days=7)
            },
        ]

        # 데이터 추가
        for mission_data in sample_missions:
            record = MissionRecord(**mission_data)
            db.session.add(record)

        db.session.commit()
        print(f"✅ {len(sample_missions)}개의 샘플 미션 기록을 추가했습니다.")

        # 메달 통계 출력
        bronze_count = MissionRecord.query.filter_by(tier='bronze').count()
        silver_count = MissionRecord.query.filter_by(tier='silver').count()
        gold_count = MissionRecord.query.filter_by(tier='gold').count()

        print(f"\n📊 메달 통계:")
        print(f"   🥉 브론즈: {bronze_count}개")
        print(f"   🥈 실버: {silver_count}개")
        print(f"   🥇 골드: {gold_count}개")

if __name__ == '__main__':
    add_sample_missions()