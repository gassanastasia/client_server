from pydantic_settings import BaseSettings
from pydantic import Field

class ClientSettings(BaseSettings):
    server_url: str = Field(default="http://localhost:8000", env="SERVER_URL")
    api_timeout: int = Field(default=10, env="API_TIMEOUT")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = ClientSettings()