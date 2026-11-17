import json
from backend.config import settings
from backend.services.ranking import search_jobs
SYSTEM = "You are CareerPilot, an honest career assistant. Ground vacancy claims in supplied job data. Never invent employers, salaries, live status or URLs. Explain uncertainty and give actionable advice."
def fallback(message,jobs,profile):
    q=(message+" "+" ".join(profile.skills or [])).lower()
    if any(w in q for w in ["job","role","intern","recommend","search","match"]):
        results=search_jobs(jobs,q,5)
        if not results: return "No close match in the demo catalogue. Try a broader query or add skills to your profile."
        return "Closest matches in the demo catalogue:\n"+"\n".join(f"- **{j.title}** at {j.company} — {j.location}, {j.work_mode}. Skills: {', '.join(j.skills[:6])} (retrieval {s:.2f})" for j,s in results)+"\n\nThese are synthetic sample listings, not verified vacancies."
    if "skill" in q or "resume" in q: return "Your saved skills: "+(", ".join(profile.skills or []) or "none yet")+". Upload a resume or update your profile to improve matching."
    return "I can help discover roles, explain matches, identify skill gaps and prepare for interviews. Configure OPENAI_API_KEY for LLM-powered tool use."
def ask_agent(message,jobs,profile):
    if not settings.openai_api_key: return fallback(message,jobs,profile),"local_fallback"
    try:
        from openai import OpenAI
        client=OpenAI(api_key=settings.openai_api_key)
        initial=search_jobs(jobs,message+" "+" ".join(profile.skills or []),5)
        context=[{"title":j.title,"company":j.company,"location":j.location,"work_mode":j.work_mode,"skills":j.skills,"description":j.description,"apply_url":j.apply_url} for j,s in initial]
        tools=[{"type":"function","function":{"name":"search_jobs","description":"Search the local demo job catalogue","parameters":{"type":"object","properties":{"query":{"type":"string"}},"required":["query"],"additionalProperties":False}}}]
        msgs=[{"role":"system","content":SYSTEM},{"role":"system","content":"Candidate profile: "+json.dumps({"skills":profile.skills,"roles":profile.preferred_roles,"locations":profile.preferred_locations})},{"role":"system","content":"Retrieved jobs: "+json.dumps(context)},{"role":"user","content":message}]
        res=client.chat.completions.create(model=settings.openai_model,messages=msgs,tools=tools,tool_choice="auto",temperature=.2)
        choice=res.choices[0]
        if choice.finish_reason=="tool_calls":
            msgs.append(choice.message)
            for call in choice.message.tool_calls:
                args=json.loads(call.function.arguments)
                found=search_jobs(jobs,args.get("query",message),5)
                data=[{"title":j.title,"company":j.company,"location":j.location,"skills":j.skills,"description":j.description,"apply_url":j.apply_url} for j,s in found]
                msgs.append({"role":"tool","tool_call_id":call.id,"content":json.dumps(data)})
            final=client.chat.completions.create(model=settings.openai_model,messages=msgs,temperature=.2)
            return final.choices[0].message.content or "No response generated.","openai_tool_call"
        return choice.message.content or "No response generated.","openai"
    except Exception as e:
        return fallback(message,jobs,profile)+f"\n\nLLM unavailable; local fallback used ({type(e).__name__}).","local_fallback"
