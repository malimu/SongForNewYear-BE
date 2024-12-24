from enum import Enum

# 카테고리 enum 정의
class CategoryEnum(Enum):
    HEALTH = "HEALTH"
    LOVE = "LOVE"
    HAPPINESS = "HAPPINESS"
    WEALTH = "WEALTH"
    SUCCESS = "SUCCESS"
    COURAGE = "COURAGE"
    LUCK = "LUCK"
    BEGINNING = "BEGINNING"

# 카테고리 목록 가져오기
def get_category_enum_list():
    return [category.value for category in CategoryEnum]