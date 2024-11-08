from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    HOST: str = Field(validation_alias="POSTGRES_HOST")
    PORT: int = Field(validation_alias="POSTGRES_PORT")
    USER: str = Field(validation_alias="POSTGRES_USER")
    PASSWORD: str = Field(validation_alias="POSTGRES_PASSWORD")
    NAME: str = Field(validation_alias="POSTGRES_DB")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def URL(self):
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"


class PostgresTestSettings(BaseSettings):
    HOST: str = Field(validation_alias="POSTGRES_HOST_TEST")
    PORT: int = Field(validation_alias="POSTGRES_PORT_TEST")
    USER: str = Field(validation_alias="POSTGRES_USER_TEST")
    PASSWORD: str = Field(validation_alias="POSTGRES_PASSWORD_TEST")
    NAME: str = Field(validation_alias="POSTGRES_DB_TEST")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def URL(self):
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"


class Settings(BaseSettings):
    PROJECT_NAME: str
    SECRET_KEY: str
    KINOPOISK_UNOFFICIAL_URL: str
    KINOPOISK_UNOFFICIAL_API_KEY: str

    DATABASE: PostgresSettings = PostgresSettings()
    DATABASE_TEST: PostgresTestSettings = PostgresTestSettings()

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
