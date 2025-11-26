from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    django_debug: bool
    django_secret_key: str

    social_auth_google_oauth2_key: SecretStr
    social_auth_google_oauth2_secret: SecretStr

    redis_host: str
    redis_port: int
    redis_db: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
