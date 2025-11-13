import google.generativeai as genai
import json
import re
from datetime import datetime, timedelta
from flask import current_app

class AIMissionGenerator:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_daily_missions(self, previous_missions=None):
        """
        매일 새로운 미션 7개를 생성합니다.
        - Bronze 3개: 3-10분
        - Silver 2개: 10-20분
        - Gold 2개: 20-40분

        Args:
            previous_missions: 전날 미션 리스트 (겹치지 않게 하기 위함)

        Returns:
            dict: 생성된 미션들
        """
        previous_missions_text = ""
        if previous_missions:
            previous_missions_text = "\n\n전날 생성된 미션들 (이와 겹치지 않게 해주세요):\n"
            for mission in previous_missions:
                previous_missions_text += f"- {mission['title']}: {mission['description']}\n"

        prompt = f"""당신은 도파민 디톡스 앱의 미션 생성 전문가입니다.
사용자가 스마트폰 중독에서 벗어나 건강한 생활을 할 수 있도록 도와주는 미션을 생성해주세요.

다음 규칙을 엄격히 지켜주세요:

1. 총 7개의 미션을 생성해야 합니다:
   - Bronze 등급 3개: 3-10분 소요
   - Silver 등급 2개: 10-20분 소요
   - Gold 등급 2개: 20-40분 소요

2. 미션은 다음 카테고리 중 하나여야 합니다:
   - physical: 신체 활동 (스트레칭, 운동, 산책 등)
   - mental: 정신 활동 (명상, 독서, 일기 등)
   - health: 건강 습관 (물 마시기, 눈 운동, 수면 등)
   - social: 사회적 활동 (가족과 대화, 친구에게 연락 등)
   - creative: 창의적 활동 (그림 그리기, 악기 연주, 요리 등)

3. 각 미션의 시간은 현실적이고 실제로 수행 가능한 시간이어야 합니다.

4. 제목은 간결하고 명확하게 (최대 20자)

5. 설명은 구체적이고 동기부여가 되도록 작성 (30-80자)

6. 매일 다양한 미션을 제공하여 사용자가 지루하지 않도록 해주세요.
{previous_missions_text}

응답은 반드시 다음 JSON 형식으로만 작성해주세요 (다른 텍스트는 포함하지 마세요):

{{
  "bronze": [
    {{"title": "미션 제목", "description": "미션 설명", "duration": 5, "category": "physical"}},
    {{"title": "미션 제목", "description": "미션 설명", "duration": 7, "category": "mental"}},
    {{"title": "미션 제목", "description": "미션 설명", "duration": 10, "category": "health"}}
  ],
  "silver": [
    {{"title": "미션 제목", "description": "미션 설명", "duration": 15, "category": "social"}},
    {{"title": "미션 제목", "description": "미션 설명", "duration": 20, "category": "creative"}}
  ],
  "gold": [
    {{"title": "미션 제목", "description": "미션 설명", "duration": 25, "category": "physical"}},
    {{"title": "미션 제목", "description": "미션 설명", "duration": 35, "category": "mental"}}
  ]
}}
"""

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()

            # JSON 추출 (코드 블록이나 다른 텍스트가 포함되어 있을 수 있음)
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                response_text = json_match.group(0)

            missions_data = json.loads(response_text)

            # 유효성 검증
            if not self._validate_missions(missions_data):
                raise ValueError("생성된 미션이 규칙을 따르지 않습니다.")

            return missions_data

        except Exception as e:
            # 로깅 (앱 컨텍스트가 있을 경우에만)
            try:
                current_app.logger.error(f"AI 미션 생성 실패: {str(e)}")
            except RuntimeError:
                print(f"AI 미션 생성 실패: {str(e)}")
            # 폴백: 기본 미션 반환
            return self._get_fallback_missions()

    def _validate_missions(self, missions_data):
        """생성된 미션의 유효성을 검증합니다."""
        try:
            # Bronze 3개, Silver 2개, Gold 2개가 있는지 확인
            if len(missions_data.get('bronze', [])) != 3:
                return False
            if len(missions_data.get('silver', [])) != 2:
                return False
            if len(missions_data.get('gold', [])) != 2:
                return False

            # Bronze 미션 시간 검증 (3-10분)
            for mission in missions_data['bronze']:
                if not (3 <= mission['duration'] <= 10):
                    return False

            # Silver 미션 시간 검증 (10-20분)
            for mission in missions_data['silver']:
                if not (10 <= mission['duration'] <= 20):
                    return False

            # Gold 미션 시간 검증 (20-40분)
            for mission in missions_data['gold']:
                if not (20 <= mission['duration'] <= 40):
                    return False

            return True

        except (KeyError, TypeError):
            return False

    def _get_fallback_missions(self):
        """API 실패 시 사용할 기본 미션"""
        return {
            "bronze": [
                {"title": "목과 어깨 스트레칭", "description": "간단한 스트레칭으로 긴장을 풀어보세요", "duration": 5, "category": "physical"},
                {"title": "깊은 호흡 연습", "description": "깊은 호흡으로 마음을 안정시켜보세요", "duration": 8, "category": "mental"},
                {"title": "물 마시기", "description": "물 한 잔을 천천히 마시며 수분을 보충하세요", "duration": 3, "category": "health"}
            ],
            "silver": [
                {"title": "짧은 산책", "description": "밖에 나가서 신선한 공기를 마시며 걸어보세요", "duration": 15, "category": "physical"},
                {"title": "독서 시간", "description": "좋아하는 책을 읽으며 휴식을 취해보세요", "duration": 20, "category": "mental"}
            ],
            "gold": [
                {"title": "명상과 집중", "description": "조용한 곳에서 집중 명상을 해보세요", "duration": 25, "category": "mental"},
                {"title": "요가 루틴", "description": "기본 요가 동작으로 몸과 마음을 정돈하세요", "duration": 30, "category": "physical"}
            ]
        }


def generate_and_save_daily_missions():
    """매일 자정에 실행될 함수 - 새로운 미션을 생성하고 저장합니다."""
    from database import db
    from models.daily_mission import DailyMission

    def log(message, level='info'):
        """로깅 헬퍼 함수"""
        try:
            if level == 'error':
                current_app.logger.error(message)
            else:
                current_app.logger.info(message)
        except RuntimeError:
            print(message)

    # Gemini API 키 가져오기
    api_key = current_app.config.get('GEMINI_API_KEY')
    if not api_key:
        log("GEMINI_API_KEY가 설정되지 않았습니다.", 'error')
        return

    # 오늘 날짜
    today = datetime.now().date()

    # 이미 오늘 미션이 생성되어 있는지 확인
    existing_mission = DailyMission.query.filter_by(date=today).first()
    if existing_mission:
        log(f"오늘({today}) 미션이 이미 생성되어 있습니다.")
        return

    # 전날 미션 가져오기 (겹치지 않게 하기 위함)
    yesterday = today - timedelta(days=1)
    previous_daily_mission = DailyMission.query.filter_by(date=yesterday).first()
    previous_missions = None
    if previous_daily_mission:
        previous_missions = previous_daily_mission.to_mission_list()

    # AI로 미션 생성
    generator = AIMissionGenerator(api_key)
    missions_data = generator.generate_daily_missions(previous_missions)

    # 데이터베이스에 저장
    daily_mission = DailyMission(
        date=today,
        bronze_1_title=missions_data['bronze'][0]['title'],
        bronze_1_description=missions_data['bronze'][0]['description'],
        bronze_1_duration=missions_data['bronze'][0]['duration'],

        bronze_2_title=missions_data['bronze'][1]['title'],
        bronze_2_description=missions_data['bronze'][1]['description'],
        bronze_2_duration=missions_data['bronze'][1]['duration'],

        bronze_3_title=missions_data['bronze'][2]['title'],
        bronze_3_description=missions_data['bronze'][2]['description'],
        bronze_3_duration=missions_data['bronze'][2]['duration'],

        silver_1_title=missions_data['silver'][0]['title'],
        silver_1_description=missions_data['silver'][0]['description'],
        silver_1_duration=missions_data['silver'][0]['duration'],

        silver_2_title=missions_data['silver'][1]['title'],
        silver_2_description=missions_data['silver'][1]['description'],
        silver_2_duration=missions_data['silver'][1]['duration'],

        gold_1_title=missions_data['gold'][0]['title'],
        gold_1_description=missions_data['gold'][0]['description'],
        gold_1_duration=missions_data['gold'][0]['duration'],

        gold_2_title=missions_data['gold'][1]['title'],
        gold_2_description=missions_data['gold'][1]['description'],
        gold_2_duration=missions_data['gold'][1]['duration'],
    )

    try:
        db.session.add(daily_mission)
        db.session.commit()
        log(f"오늘({today}) 미션이 성공적으로 생성되었습니다.")
    except Exception as e:
        db.session.rollback()
        log(f"미션 저장 실패: {str(e)}", 'error')