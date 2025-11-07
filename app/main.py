from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.routers import spc_part_master_router

app = FastAPI(title="Aoyama Supply Chain Backend", version="1.0")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://10.17.3.244:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(spc_part_master_router.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to Aoyama Supply Chain API"}