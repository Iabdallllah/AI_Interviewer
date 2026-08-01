from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI ECO Service"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 5000

    class Config:
        env_file = ".env"


settings = Settings()
