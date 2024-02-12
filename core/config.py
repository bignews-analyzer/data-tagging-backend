from pydantic import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    MYSQL_URL: str = os.environ.get('MYSQL_URL')

    ACCESS_TOKEN_ENCODE_ALGORITHM: str = os.environ.get('ACCESS_TOKEN_ENCODE_ALGORITHM')
    ACCESS_SECRET_KEY: str = os.environ.get('ACCESS_SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 2

    REFRESH_TOKEN_ENCODE_ALGORITHM: str = os.environ.get('REFRESH_TOKEN_ENCODE_ALGORITHM')
    REFRESH_SECRET_KEY: str = os.environ.get('REFRESH_SECRET_KEY')
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 14

    PASSWORD_SALT: str = os.environ.get('PASSWORD_SALT')

    class Config:
        case_sensitive = True


settings = Settings()
