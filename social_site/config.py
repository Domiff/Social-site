from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    django_debug: bool
    django_secret_key: str

    social_auth_google_oauth2_key: SecretStr
    social_auth_google_oauth2_secret: SecretStr

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
