from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class BaseModel:
    @declared_attr
    def __tablename__(cls) -> str:
        """테이블 이름을 자동으로 클래스 이름으로 설정"""
        return cls.__name__.lower()

    createdAt = Column(DateTime, default=datetime.utcnow, nullable=False)  # 생성 시간
    modifiedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)  # 수정 시간