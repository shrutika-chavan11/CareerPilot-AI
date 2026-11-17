from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    database_url: str = "sqlite:///./careerpilot.db"
    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"
    use_sentence_transformers: bool = False
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
settings = Settings()
