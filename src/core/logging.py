import logging
import sys
from settings import settings  # settings.py 파일에서 환경 설정을 가져옵니다.

# 로깅 설정 함수
def setup_logging():
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO  # DEBUG 모드일 때 더 자세한 로그 출력

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),  # 콘솔에 로그 출력
            logging.FileHandler("app.log")      # 파일에 로그 기록
        ]
    )

    logger = logging.getLogger(__name__)
    logger.info("로깅 설정 완료")
    return logger

# 로깅 설정 적용
logger = setup_logging()