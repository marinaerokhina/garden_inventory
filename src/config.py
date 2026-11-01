"""Local PostgreSQL configuration loaded from an untracked .env file."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

DB_NAME = os.getenv("DB_NAME", "inventory_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))


def require_db_password():
    password = os.getenv("DB_PASSWORD")
    if not password:
        raise RuntimeError(
            "DB_PASSWORD is not configured. Copy .env.example to .env "
            "and set your local PostgreSQL password."
        )
    return password


def database_url(database=None):
    """Build a correctly escaped SQLAlchemy URL for a local database."""
    return URL.create(
        "postgresql+psycopg2",
        username=DB_USER,
        password=require_db_password(),
        host=DB_HOST,
        port=DB_PORT,
        database=database or DB_NAME,
    )
