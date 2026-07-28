from fastapi import FastAPI

from routers.auth import router as auth_router
from routers.rooms import router as rooms_router

app = FastAPI(title="E-commerce & Retail (Multimodal RAG Platform )")

app.include_router(auth_router)
app.include_router(rooms_router)


@app.get("/")
def root():
    return {"message": "Multimodal RAG API is running"}