import logging
import sys

# 로깅 설정 함수
def setup_logging():
    log_level = logging.DEBUG

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