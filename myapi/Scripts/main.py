from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "안녕하세요"}