from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./sql_app.sqlite"

    SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()