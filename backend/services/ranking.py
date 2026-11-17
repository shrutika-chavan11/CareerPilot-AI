from backend.services.embeddings import get_retriever
def doc(job):
    return " ".join([job.title,job.company,job.location,job.work_mode,job.description," ".join(job.skills or [])])
def search_jobs(jobs, query, k=10):
    engine=get_retriever(); engine.fit([doc(j) for j in jobs])
    return [(jobs[i],float(s)) for i,s in engine.search(query,k)]
def recommend_jobs(jobs, profile, k=10):
    query=" ".join((profile.skills or [])+(profile.preferred_roles or [])+(profile.preferred_locations or [])) or "internship"
    retrieved=search_jobs(jobs,query,max(k,len(jobs)))
    skills={x.lower() for x in (profile.skills or [])}
    locs=[x.lower() for x in (profile.preferred_locations or [])]
    modes=[x.lower() for x in (profile.preferred_work_modes or [])]
    out=[]
    for job,sem in retrieved:
        js={x.lower() for x in (job.skills or [])}; matched=sorted(skills & js)
        overlap=len(matched)/max(1,len(skills)) if skills else 0
        loc=1 if not locs or any(x in job.location.lower() for x in locs) else 0
        mode=1 if not modes or job.work_mode.lower() in modes else 0
        score=.55*max(0,min(1,sem))+.30*overlap+.10*loc+.05*mode
        out.append({"job":job,"score":round(score,4),"matched_skills":matched})
    return sorted(out,key=lambda x:x["score"],reverse=True)[:k]
