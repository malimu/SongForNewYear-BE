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
    tag_enum = get_tag_enum_list()

    # 태그별 노래 목록 가져오기
    total_songs = []
    for tag in tag_enum:
        songs = await get_songs_by_tag(tag, skip=0, limit=100)
        tag_songs = [{"title": song["title"], "idx": song["song_index"]} for song in songs]
        total_songs.append({
            "category": tag,
            "songs": tag_songs
        })

    # 프롬프트
    prompt = f'''
    당신은 사용자의 소원을 듣고 그것을 다음 8가지 카테고리 중 하나로 분류한 뒤, 제목을 바탕으로 가장 적합한 노래를 골라줍니다.
    소원의 핵심 내용을 이해하고 단 한 곡을 선택해야 합니다.
    * category 값은 다음 중 하나입니다: {", ".join(tag_enum)}

    * OUTPUT 형태 및 자료형:
    {{
      \"idx\": int
    }}

    아래 INPUT의 total_songs중 wish를 이루어줄 노래를 1개 골라 OUTPUT 형태에 맞게 응답하세요.
    * INPUT:
    {{
      "wish": "{content}",
      "total_songs": {json.dumps(total_songs)}
    }}
    '''

    # OpenAI ChatGPT API 호출
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
            temperature=0.0
        )
        
        # Extracting the content from the response
        message_content = response.choices[0].message.content
        
        print(response.choices[0].message.content)

        # Parsing the response JSON (the response is expected to be in valid JSON format)
        response_json = json.loads(message_content)

        # Extracting required data
        song_index = response_json.get("idx")

        # Validating the response
        if song_index is None:
            raise ValueError("Invalid response format: Missing required keys.")

        # Returning the result
        return {
            "song_index": song_index
        }

    except json.JSONDecodeError as e:
        error_message = f"JSON Decode Error: {e}\n{traceback.format_exc()}"
        logging.error(error_message)
        raise CustomException(ErrorCode.INTERNAL_SERVER_ERROR)

    except Exception as e:
        error_message = f"Exception occurred: {e}\n{traceback.format_exc()}"
        logging.error(error_message)
        raise CustomException(ErrorCode.EXTERNAL_SERVICE_ERROR)