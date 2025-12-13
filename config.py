import os
import psycopg2
from dotenv import load_dotenv
from supabase import create_client, Client
from os import getenv

SECRET_KEY = getenv("SECRET_KEY")
DB_NAME= getenv("DB_NAME")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT", "5432")
def get_db_connection():
    """
    Establishes and returns a new psycopg2 database connection.
    Must be called within a try/finally block to ensure connection closure.
    """
    if not all([DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT]):
        raise ValueError("Missing PostgreSQL database credentials in environment variables.")
        
    return psycopg2.connect(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST, 
        port=DB_PORT
    )

SUPABASE_URL = getenv("SUPABASE_URL")
SUPABASE_KEY = getenv("SUPABASE_KEY")
SUPABASE_BUCKET = getenv("SUPABASE_BUCKET", 'picture')

supabase: Client = None
SUPABASE_BASE_URL: str = None

if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("Supabase client initialized successfully for storage.")
        
        SUPABASE_BASE_URL = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/"

    except Exception as e:
        print(f"Failed to initialize Supabase client: {e}")