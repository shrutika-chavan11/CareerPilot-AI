import json
from pathlib import Path
from backend.models import Job
def seed_jobs(db):
    if db.query(Job).count(): return
    path = Path(__file__).resolve().parents[1] / "data" / "sample_jobs.json"
    for item in json.loads(path.read_text(encoding="utf-8")): db.add(Job(**item))
    db.commit()
