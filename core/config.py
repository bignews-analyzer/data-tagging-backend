from pydantic import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    MYSQL_URL = os.environ.get('MYSQL_URL')

    class Config:
        case_sensitive = True


settings = Settings()
