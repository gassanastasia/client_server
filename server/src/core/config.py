from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Database
    db_url: str = Field(default="sqlite+aiosqlite:///./requests.db", env="DATABASE_URL")
    db_echo: bool = Field(default=True, env="DB_ECHO")
    
    # Server
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    
    # CORS
    cors_origins: list[str] = Field(default=["*"])
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()