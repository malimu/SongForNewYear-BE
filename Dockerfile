FROM python:3.11

COPY ./src /src
WORKDIR /src

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]