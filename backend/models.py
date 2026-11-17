from datetime import datetime
from sqlalchemy import String, Text, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from backend.database import Base
class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    company: Mapped[str] = mapped_column(String(160))
    location: Mapped[str] = mapped_column(String(160), default="India")
    work_mode: Mapped[str] = mapped_column(String(40), default="Remote")
    description: Mapped[str] = mapped_column(Text)
    skills: Mapped[list] = mapped_column(JSON, default=list)
    job_type: Mapped[str] = mapped_column(String(80), default="Internship")
    apply_url: Mapped[str] = mapped_column(String(500), default="")
class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), default="Candidate")
    email: Mapped[str] = mapped_column(String(200), default="")
    skills: Mapped[list] = mapped_column(JSON, default=list)
    preferred_roles: Mapped[list] = mapped_column(JSON, default=list)
    preferred_locations: Mapped[list] = mapped_column(JSON, default=list)
    preferred_work_modes: Mapped[list] = mapped_column(JSON, default=list)
    resume_text: Mapped[str] = mapped_column(Text, default="")
class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(String(20))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
