from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings) : 
     SECRET_KEY: str
     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
     ALGORITHM: str = "HS256"
    
     class Config: 
          env_file = BASE_DIR / ".env",     
          extra = "ignore"


settings = Settings() 