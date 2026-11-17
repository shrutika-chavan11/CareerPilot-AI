import os, requests, streamlit as st
API=os.getenv("API_BASE_URL","http://127.0.0.1:8000")
st.set_page_config(page_title="CareerPilot AI",page_icon="🚀",layout="wide")
st.markdown("""
<style>
.stApp{background:#0b1020;color:#eef2ff}
[data-testid="stSidebar"]{background:#111a30}
.block-container{padding-top:1.8rem;max-width:1250px}
.hero{padding:1.5rem 1.8rem;border:1px solid #273653;border-radius:18px;background:linear-gradient(120deg,#172554,#312e81 65%,#164e63);margin-bottom:1.2rem}
.hero h1{color:white;margin:0}.hero p{color:#dbeafe;margin-bottom:0}
.job{border:1px solid #263653;background:#111a30;border-radius:14px;padding:1rem 1.1rem;margin-bottom:.8rem}
.muted{color:#a5b4cf;font-size:.9rem}
.skill{display:inline-block;border:1px solid #3b4d70;border-radius:20px;padding:3px 9px;margin:3px;color:#bfdbfe;font-size:.78rem}
</style>
""",unsafe_allow_html=True)
def api(method,path,**kwargs):
    try:
        r=requests.request(method,f"{API}{path}",timeout=45,**kwargs); r.raise_for_status(); return r.json()
    except requests.RequestException as e:
        st.error(f"Cannot reach API at {API}. Start FastAPI first. {e}"); return None
def card(j):
    tags=" ".join(f'<span class="skill">{s}</span>' for s in (j.get("skills") or [])[:8])
    score=j.get("score"); suffix=f" · Match score: {score:.2f}" if isinstance(score,(int,float)) else ""
    st.markdown(f'<div class="job"><h3 style="margin:0;color:#f8fafc">{j["title"]}</h3><div class="muted">{j["company"]} · {j["location"]} · {j["work_mode"]}{suffix}</div><p>{j["description"]}</p>{tags}</div>',unsafe_allow_html=True)
    if j.get("apply_url","").startswith("http"): st.markdown(f"[Demo listing link]({j['apply_url']})")
st.markdown('<div class="hero"><h1>🚀 CareerPilot AI</h1><p>Your AI-powered career companion — understand your profile, discover relevant roles, and plan your next move.</p></div>',unsafe_allow_html=True)
pages=["Overview","Resume & Profile","Explore Jobs","Recommendations","Career Agent","Evaluation"]
page=st.sidebar.radio("Workspace",pages); st.sidebar.caption("CareerPilot AI · Portfolio MVP")
if api("GET","/health"): st.sidebar.success("API connected")
if page=="Overview":
    st.subheader("Your career command centre")
    p=api("GET","/profile") or {}; jobs=api("GET","/jobs") or []; rec=api("GET","/recommendations?top_k=5") or []
    a,b,c=st.columns(3); a.metric("Jobs in catalogue",len(jobs)); b.metric("Profile skills",len(p.get("skills",[]))); c.metric("Recommendations",len(rec))
    st.markdown("### Recommended for you")
    if rec:
        for j in rec[:3]: card(j)
    else: st.info("Upload your resume or add skills to your profile.")
    st.caption("Sample listings are synthetic, not verified live vacancies.")
elif page=="Resume & Profile":
    st.subheader("Build your candidate profile")
    f=st.file_uploader("Upload resume",type=["pdf","docx","txt"])
    if f and st.button("Parse resume",type="primary"):
        x=api("POST","/resume/parse",files={"file":(f.name,f.getvalue(),f.type)})
        if x:
            st.success(f"Extracted {x['characters_extracted']} characters")
            st.write("Detected skills:",x["detected_skills"])
            with st.expander("Text preview"): st.text(x["preview"])
    p=api("GET","/profile") or {}
    with st.form("profile"):
        name=st.text_input("Name",p.get("name","Candidate")); email=st.text_input("Email",p.get("email",""))
        skills=st.text_input("Skills (comma separated)",", ".join(p.get("skills",[])))
        roles=st.text_input("Preferred roles (comma separated)",", ".join(p.get("preferred_roles",[])))
        locs=st.text_input("Preferred locations (comma separated)",", ".join(p.get("preferred_locations",[])))
        modes=st.multiselect("Work modes",["Remote","Hybrid","On-site"],default=p.get("preferred_work_modes",[]))
        save=st.form_submit_button("Save profile",type="primary")
    if save:
        payload={"name":name,"email":email,"skills":[x.strip() for x in skills.split(",") if x.strip()],"preferred_roles":[x.strip() for x in roles.split(",") if x.strip()],"preferred_locations":[x.strip() for x in locs.split(",") if x.strip()],"preferred_work_modes":modes}
        if api("PUT","/profile",json=payload): st.success("Profile saved.")
elif page=="Explore Jobs":
    st.subheader("Search the job catalogue")
    q=st.text_input("Describe your target role",placeholder="Python backend internship involving LLMs, RAG and semantic search")
    k=st.slider("Results",1,15,8)
    if st.button("Search",type="primary") and q.strip():
        rows=api("POST","/search",json={"query":q,"top_k":k})
        if rows:
            st.write(f"{len(rows)} demo listings")
            for j in rows: card(j)
elif page=="Recommendations":
    st.subheader("Personalized recommendations")
    st.caption("Baseline weighted ranking: retrieval, skill overlap, location and work mode.")
    rows=api("GET","/recommendations?top_k=15") or []
    for j in rows:
        card(j)
        if j.get("matched_skills"): st.caption("Matched skills: "+", ".join(j["matched_skills"]))
elif page=="Career Agent":
    st.subheader("Talk to CareerPilot")
    st.caption("Ask for matching roles, skill gaps or interview preparation.")
    if "chat_messages" not in st.session_state: st.session_state.chat_messages=api("GET","/chat/history?limit=40") or []
    for m in st.session_state.chat_messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    prompt=st.chat_input("Find roles matching Python, SQL and my interest in LLMs...")
    if prompt:
        st.session_state.chat_messages.append({"role":"user","content":prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result=api("POST","/chat",json={"message":prompt})
                if result:
                    st.markdown(result["answer"]); st.caption("Agent mode: "+result["mode"])
                    st.session_state.chat_messages.append({"role":"assistant","content":result["answer"]})
    if st.button("Clear chat"):
        api("DELETE","/chat/history"); st.session_state.chat_messages=[]; st.rerun()
elif page=="Evaluation":
    st.subheader("Retrieval evaluation")
    st.write("Run the small hand-labelled demo smoke test.")
    if st.button("Run evaluation",type="primary"):
        rows=api("POST","/evaluation/run") or []
        for x in rows:
            with st.container(border=True):
                st.markdown("**Query:** "+x["query"])
                a,b=st.columns(2); a.metric("Precision@5",f'{x["precision_at_5"]:.2f}'); b.metric("Recall@5",f'{x["recall_at_5"]:.2f}')
                st.write("Ranked:",x["results"])
        st.warning("Tiny synthetic evaluation set only; not production evidence.")
