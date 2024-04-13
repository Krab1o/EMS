from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BOT_TOKEN: str

    class Config:
        env_file = r"C:\Users\esvinarev\Desktop\ems\ems\components\botBySvinarevEA_0_0_1\.env"
        extra = "allow"


settings = Settings()