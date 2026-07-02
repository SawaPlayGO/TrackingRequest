from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Settings
    HOST_API: str = "0.0.0.0"
    PORT_API: int = 8000

    # DB
    DB_NAME: str = "app"  # {DB_NAME}.db

    @property
    def DB_URL(self) -> str:
        return f"sqlite+aiosqlite:///./{self.DB_NAME}.db"


settings = Settings()
