FROM python:3.11

WORKDIR /code

COPY ./src/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./src /code/src

# Upgrade pip to the latest version
RUN pip install --upgrade pip

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]