# utils/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_PATH: str
    RAW_DATA_PATH: str
    MISTRAL_API_KEY: str
    PINECONE_KEY: str
    PINECONE_HOST: str
    PINECONE_INDEX_NAME: str
    EMBEDDING_MODEL: str
    
    
    # Tell pydantic-settings to load from .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Create a singleton instance
settings = Settings() # type: ignore