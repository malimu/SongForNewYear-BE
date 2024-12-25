from enum import Enum

# 태그 enum 정의
class TagEnum(Enum):
    SPECIAL = "SPECIAL"
    ENDURANCE = "ENDURANCE"
    CONFIDENCE = "CONFIDENCE"
    BODY_HEALTH = "BODY_HEALTH"
    MENTAL_HEALTH = "MENTAL_HEALTH"
    RETRY = "RETRY"
    YOUTH = "YOUTH"
    NEW_START = "NEW_START"
    MONEY = "MONEY"
    LOTTO = "LOTTO"
    HOUSE = "HOUSE"
    LOVE_START = "LOVE_START"
    LOVE_KEEP = "LOVE_KEEP"
    HAPPINESS = "HAPPINESS"
    SUCCESS = "SUCCESS"
    LUCK = "LUCK"
    MEAL = "MEAL"

# 태그 목록 가져오기
def get_tag_enum_list():
    return [tag.value for tag in TagEnum]