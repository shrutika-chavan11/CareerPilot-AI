from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import Base,engine,SessionLocal
from backend.seed import seed_jobs
from backend.api.routes import router
app=FastAPI(title="CareerPilot AI",version="1.0.0",description="AI career discovery API")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:8501","http://127.0.0.1:8501"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(router)
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine); db=SessionLocal()
    try: seed_jobs(db)
    finally: db.close()
@app.get("/")
def root(): return {"message":"Welcome to CareerPilot AI","docs":"/docs"}
