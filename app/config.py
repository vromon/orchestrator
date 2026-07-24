from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    PINECONE_API: str | None = None
    GEMINI_API: str | None = None
    TRIP_INDEX: str | None = None
    DB_CONNECTION: str | None = None

settings = Settings()