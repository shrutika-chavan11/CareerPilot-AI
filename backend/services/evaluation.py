from backend.database import SessionLocal, Base, engine
from backend.seed import seed_jobs
from backend.models import Job
from backend.services.ranking import search_jobs
CASES=[("Python LLM agent RAG backend",{"AI/LLM Engineering Intern"}),("semantic search recommendation ranking",{"Search and Recommendation Intern"}),("React Node frontend full stack",{"Full Stack Developer Intern"})]
def score_at_k(titles,relevant,k=5):
    hits=sum(t in relevant for t in titles[:k])
    return hits/k if k else 0, hits/len(relevant) if relevant else 0
def run():
    db=SessionLocal()
    try:
        jobs=db.query(Job).all(); rows=[]
        for q,rel in CASES:
            titles=[j.title for j,s in search_jobs(jobs,q,5)]
            p,r=score_at_k(titles,rel); rows.append({"query":q,"precision_at_5":p,"recall_at_5":r,"results":titles})
        return rows
    finally: db.close()
if __name__=="__main__":
    Base.metadata.create_all(engine); db=SessionLocal(); seed_jobs(db); db.close()
    for row in run(): print(row)
