from pydantic_settings import BaseSettings
import urllib.parse

class Settings(BaseSettings):
    # Database configuration - these can come from .env
    DB_HOST: str = "localhost"
    DB_USER: str = "root"
    DB_PASSWORD: str = "Rev2005@!!"
    DB_PORT: str = "3306"
    DB_NAME: str = "ai_support_db"
    DATABASE_URL: str = None  # Can be provided directly in .env
    
    @property
    def effective_database_url(self) -> str:
        """Return the database URL (either from .env or built from individual fields)"""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        encoded_password = urllib.parse.quote_plus(self.DB_PASSWORD)
        return f"mysql+pymysql://{self.DB_USER}:{encoded_password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    LLAMA_BASE_URL: str = "https://aimodels.jadeglobal.com:8082/ollama/api"
    LLAMA_MODEL: str = "deepseek-coder:6.7b"
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Allow extra fields

settings = Settings()
