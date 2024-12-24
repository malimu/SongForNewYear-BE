FROM python:3.11

WORKDIR /src

COPY ./src /src

RUN pip install --no-cache-dir -r /src/requirements.txt

# Upgrade pip to the latest version
RUN pip install --upgrade pip

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]