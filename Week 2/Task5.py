from fastapi import FastAPI

app = FastAPI()

@app.post("/ping", status_code=201)
def ping():
    return {"status": "created"}