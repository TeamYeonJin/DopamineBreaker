MISSIONS = [
    {
        "id": 1,
        "title": "목과 어깨 스트레칭",
        "description": "간단한 목과 어깨 스트레칭으로 긴장을 풀어보세요",
        "duration": 5,
        "tier": "bronze",
        "category": "physical",
    },
    {
        "id": 2,
        "title": "깊은 호흡",
        "description": "깊은 호흡으로 마음을 안정시켜보세요",
        "duration": 10,
        "tier": "bronze",
        "category": "mental",
    },
    {
        "id": 3,
        "title": "수분 보충",
        "description": "물 한 잔을 천천히 마시며 수분을 보충하세요",
        "duration": 3,
        "tier": "bronze",
        "category": "health",
    },
    {
        "id": 4,
        "title": "독서 휴식",
        "description": "좋아하는 책을 읽으며 휴식을 취해보세요",
        "duration": 20,
        "tier": "silver",
        "category": "mental",
    },
    {
        "id": 5,
        "title": "짧은 산책",
        "description": "밖에 나가서 짧은 산책을 즐겨보세요",
        "duration": 15,
        "tier": "silver",
        "category": "physical",
    },
    {
        "id": 6,
        "title": "기본 요가",
        "description": "기본 요가 동작으로 몸과 마음을 정돈하세요",
        "duration": 30,
        "tier": "gold",
        "category": "physical",
    },
    {
        "id": 7,
        "title": "집중 명상",
        "description": "긴 시간 동안 집중 명상을 해보세요",
        "duration": 25,
        "tier": "gold",
        "category": "mental",
    },
]


def get_mission_presets():
    """Return the editable preset mission list."""
    return MISSIONS
