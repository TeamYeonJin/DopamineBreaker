#!/usr/bin/env python3
"""AI 미션 생성 테스트 스크립트"""

from services.ai_mission_generator import AIMissionGenerator
from config import Config
import json

def test_mission_generation():
    """AI 미션 생성 테스트"""
    api_key = Config.GEMINI_API_KEY

    if not api_key:
        print("❌ GEMINI_API_KEY가 설정되지 않았습니다.")
        return

    print("🤖 AI 미션 생성 테스트 시작...")
    print(f"API Key: {api_key[:10]}...")

    generator = AIMissionGenerator(api_key)

    try:
        # 미션 생성
        missions_data = generator.generate_daily_missions()

        print("\n✅ 미션 생성 성공!\n")
        print("=" * 60)
        print("📋 생성된 미션:")
        print("=" * 60)

        # Bronze 미션
        print("\n🥉 Bronze 미션 (3개):")
        for i, mission in enumerate(missions_data['bronze'], 1):
            print(f"  {i}. {mission['title']} ({mission['duration']}분)")
            print(f"     {mission['description']}")
            print(f"     카테고리: {mission['category']}\n")

        # Silver 미션
        print("🥈 Silver 미션 (2개):")
        for i, mission in enumerate(missions_data['silver'], 1):
            print(f"  {i}. {mission['title']} ({mission['duration']}분)")
            print(f"     {mission['description']}")
            print(f"     카테고리: {mission['category']}\n")

        # Gold 미션
        print("🥇 Gold 미션 (2개):")
        for i, mission in enumerate(missions_data['gold'], 1):
            print(f"  {i}. {mission['title']} ({mission['duration']}분)")
            print(f"     {mission['description']}")
            print(f"     카테고리: {mission['category']}\n")

        print("=" * 60)

        # JSON 형식으로도 출력
        print("\n📄 JSON 형식:")
        print(json.dumps(missions_data, ensure_ascii=False, indent=2))

    except Exception as e:
        print(f"\n❌ 미션 생성 실패: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_mission_generation()