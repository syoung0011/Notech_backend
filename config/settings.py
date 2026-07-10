from pydantic_settings import BaseSettings, SettingsConfigDict


class DB_Settings(BaseSettings):
    host:str
    port:str
    user:str
    password:str
    name:str
    charset:str

    @property
    def url(self) -> str:
        return (f"mysql+aiomysql://{self.user}:{self.password}"
                f"@{self.host}:{self.port}/{self.name}?charset={self.charset}")

class JWT_Settings(BaseSettings):
    secret_key:str
    algorithm:str
    hour_delta:int

class AppSettings(BaseSettings):
    db: DB_Settings
    jwt:JWT_Settings

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore"
    )

settings = AppSettings()