import os
from pathlib import Path
from dotenv import load_dotenv

# Always load .env from the same folder as this file
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SECRET_KEY   = os.getenv("SECRET_KEY", "fallback-secret-key")
ADMIN_EMAIL  = os.getenv("ADMIN_EMAIL", "santoshravi.san.2004@gmail.com")
