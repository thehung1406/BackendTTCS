from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    SECRET_KEY: str
    ALGORITHM: str

    DATABASE_URL: str
    POSTGRES_USER : str
    POSTGRES_PASSWORD : str
    POSTGRES_DB : str
    FRONTEND_URL : str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    CORS_ORIGINS: str
settings = Settings()
