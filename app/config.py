from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")
    PINECONE_API:str
    GEMINI_API:str
    TRIP_INDEX:str
    DB_CONNECTION:str
settings=Settings()