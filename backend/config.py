from dotenv import load_dotenv
import os
from pathlib import Path


env_path = Path(__file__).cwd()
env_file_path = env_path.joinpath(".env")

load_dotenv(env_file_path)


class Envs:
    DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DATABASE_HOST = os.getenv("DATABASE_HOST")
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    SECRET_KEY = os.getenv("SECRET_KEY", "9b3d9cd5a17a6e3583c7226f2475127746e788cd8651c9bf62066cad3c8b20f7")
    SSO_MICROSOFT_CLIENT_ID = os.getenv("SSO_MICROSOFT_CLIENT_ID")
    SSO_MICROSOFT_CLIENT_SECRET = os.getenv("SSO_MICROSOFT_CLIENT_SECRET")
    SSO_MICROSOFT_CLIENT_TENANT = os.getenv("SSO_MICROSOFT_CLIENT_TENANT")
    SSO_MICROSOFT_CLIENT_REDIRECT_URI = os.getenv("SSO_MICROSOFT_CLIENT_REDIRECT_URI")
    SSO_GOOGLE_CLIENT_ID = os.getenv("SSO_GOOGLE_CLIENT_ID")
    SSO_GOOGLE_CLIENT_SECRET = os.getenv("SSO_GOOGLE_CLIENT_SECRET")
    SSO_GOOGLE_CLIENT_TENANT = os.getenv("SSO_GOOGLE_CLIENT_TENANT")
    SSO_GOOGLE_CLIENT_REDIRECT_URI = os.getenv("SSO_GOOGLE_CLIENT_REDIRECT_URI")
    DEFAULT_LIMIT = os.getenv("DEFAULT_LIMIT", "180/minute")

    ENV = os.getenv("ENV")
    FRONTEND_URL = os.getenv("FRONTEND_URL")

    EMAIL_ADMIN = os.getenv("EMAIL_ADMIN")

    # @staticmethod
    # def get_config():
    #     try:

    #         query = select(Configs)
    #         return (ctx.execute(query)).scalar_one_or_none()
    #     except Exception:
    #         return {"message": "Key is not exist"}


# SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{Envs.DATABASE_USERNAME}:{Envs.DATABASE_PASSWORD}@{Envs.DATABASE_HOST}:{Envs.POSTGRES_PORT}/{Envs.DATABASE_NAME}"
SQLALCHEMY_DATABASE_URL = os.environ.get(
    # "SQLALCHEMY_DATABASE_URL", "sqlite+aiosqlite:///rosie_app.db"
    "SQLALCHEMY_DATABASE_URL", "postgresql+asyncpg://dipo:Saonhon0i@103.72.99.35:5432/slope_dev"
)
# SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://postgres:VuNguy3n1@localhost:5432/vutest"

SECRET_KEY = f"{Envs.SECRET_KEY}"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

HERE = Path(__file__).parent.absolute()
STATIC = f"{HERE}/client/static"
STORAGE = f"{HERE}/storage"
UPLOAD_IMAGE_PATH = f"{STORAGE}/images"
UPLOAD_FOLDER_PATH = f"{STORAGE}/uploads"
VECTOR_FOLDER_PATH = f"{STORAGE}/vectors"
EXPERTS_FOLDER_PATH = f"{STORAGE}/experts"
DOCUMENT_FOLDER_PATH = f"{STORAGE}/documents"
TMP_FOLDER_PATH = f"{STORAGE}/tmp"

FRONTEND_URL = os.environ.get("FRONTEND_URL")
