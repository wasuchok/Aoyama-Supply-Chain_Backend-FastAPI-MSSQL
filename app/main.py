from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers import spc_part_master_router

app = FastAPI(title="Aoyama Supply Chain Backend", version="1.0")

app.include_router(spc_part_master_router.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to Aoyama Supply Chain API"}