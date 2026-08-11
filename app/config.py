from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
<<<<<<< HEAD
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")
    PINECONE_API:str
    GEMINI_API:str
    TRIP_INDEX:str
    DB_CONNECTION:str
    UPSTASH_REDIS_REST_URL:str
    UPSTASH_REDIS_REST_TOKEN:str
settings=Settings()
=======
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    PINECONE_API: str | None = None
    GEMINI_API: str | None = None
    TRIP_INDEX: str | None = None
    DB_CONNECTION: str | None = None

settings = Settings()
>>>>>>> 17a7a6ffcd8cedeb436a351cc5c6880743e6cfea
