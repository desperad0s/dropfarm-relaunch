from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Dropfarm"
    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    BROWSER_DATA_DIR: str = "browser_data"

    class Config:
        env_file = ".env"

settings = Settings()