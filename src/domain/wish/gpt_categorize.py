from openai import OpenAI
from dotenv import load_dotenv
import os
import traceback
import logging
import json

from src.domain.song.tag import get_tag_enum_list
from src.domain.song.services import get_songs_by_tag
from src.exceptions.custom_exceptions import CustomException
from src.exceptions.error_codes import ErrorCode

load_dotenv()

openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def categorize_wish(content: str) -> dict:
    # 태그 Enum 목록 가져오기
    tag_enum = [tag for tag in get_tag_enum_list() if tag != "SPECIAL"]

    # 태그별 노래 목록 가져오기
    total_songs = []
    for tag in tag_enum:
        songs = await get_songs_by_tag(tag, skip=0, limit=100)
        tag_songs = [{"lyrics": song["lyrics"], "tag": tag, "idx": song["song_index"]} for song in songs]
        total_songs.append({
            "category": tag,
            "songs": tag_songs
        })

    # 프롬프트
    prompt = f'''
    당신은 사용자의 소원을 듣고 그것을 다음 tag 중 하나로 분류합니다.
    * tag 값은 다음 중 하나입니다: {", ".join(tag_enum)}

    * OUTPUT 형태 및 자료형:
    정확히 다음과 같은 JSON 형식으로 반환해야 합니다:
    {{
      "tag": "값"
    }}

    아래 INPUT에 대해 적합한 tag를 골라 반환하세요:
    * INPUT:
    {{
      "wish": "{content}"
    }}
    '''

    # OpenAI ChatGPT API 호출
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=30,
            temperature=0.0
        )
        
        # Extracting the content from the response
        message_content = response.choices[0].message.content
        print("GPT Response:", message_content) # 디버깅용

        # 코드 블록 제거
        if message_content.startswith("```"):
            message_content = message_content.split("```")[1].strip()

        # JSON 파싱
        response_json = json.loads(message_content)
        tag = response_json.get("tag")

        # 태그 검증
        if tag is None:
            raise ValueError("Invalid response format: 'tag' key is missing.")
        
        return {"tag": tag}

    except json.JSONDecodeError as e:
        error_message = f"JSON Decode Error: {e}\n{traceback.format_exc()}"
        logging.error(error_message)
        raise CustomException(ErrorCode.INTERNAL_SERVER_ERROR)

    except Exception as e:
        error_message = f"Exception occurred: {e}\n{traceback.format_exc()}"
        logging.error(error_message)
        raise CustomException(ErrorCode.EXTERNAL_SERVICE_ERROR)