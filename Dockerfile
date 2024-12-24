FROM python:3.11

COPY ./src /src
WORKDIR /src

RUN pip install -r requirements.txt

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Set PYTHONPATH to /src to include the src directory in the module path
ENV PYTHONPATH=/src

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]