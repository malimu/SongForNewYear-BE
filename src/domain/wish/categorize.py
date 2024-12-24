from openai import OpenAI
from dotenv import load_dotenv
import os

from src.exceptions.custom_exceptions import CustomException
from src.exceptions.error_codes import ErrorCode

load_dotenv()

openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def categorize_wish(content: str) -> str:
    # 프롬프트
    prompt = f"""
    당신은 사용자의 소원을 듣고 그것을 다음 8가지 카테고리 중 하나로 분류하는 역할을 합니다: HEALTH, LOVE, HAPPINESS, WEALTH, SUCCESS, COURAGE, LUCK, BEGINNING.

    사용자가 소원을 말하면, 그 소원의 핵심 내용을 이해하고 가장 적절한 하나의 카테고리로 분류합니다.
    소원이 여러 카테고리에 걸쳐 있을 경우, 중심적인 의미를 반영하여 단 하나의 카테고리로만 선택합니다.

    예시 소원 및 분류 결과:
    소원: "건강하게 오래 살고 싶어요."
    분류: HEALTH
    소원: "애인을 만나고 싶어요."
    분류: LOVE
    소원: "복권에 당첨되고 싶어요."
    분류: WEALTH

    사용자가 말한 소원은 다음과 같습니다:
    소원: "{content}"
    분류:
    """
    
    # OpenAI ChatGPT API 호출
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
            temperature=0.0
        )
        # GPT의 응답에서 카테고리 추출
        category = response.choices[0].message.content.strip()
        return category
    except Exception as e:
        raise CustomException(
            error_code=ErrorCode.EXTERNAL_SERVICE_ERROR, 
            status_code=500)
