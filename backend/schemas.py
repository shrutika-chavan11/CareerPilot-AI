from pydantic import BaseModel, Field
class ProfileUpdate(BaseModel):
    name: str = "Candidate"
    email: str = ""
    skills: list[str] = Field(default_factory=list)
    preferred_roles: list[str] = Field(default_factory=list)
    preferred_locations: list[str] = Field(default_factory=list)
    preferred_work_modes: list[str] = Field(default_factory=list)
class SearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=1000)
    top_k: int = Field(default=10, ge=1, le=50)
class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
