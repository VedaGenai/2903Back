import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:Temp1234@localhost:5432/fasthire"
)

# Google AI Configuration
GOOGLE_API_KEY = os.getenv("API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.0-flash")
MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", 0.7))

# Database Pool Settings
DATABASE_POOL_SIZE = int(os.getenv("DATABASE_POOL_SIZE", 10))
DATABASE_MAX_OVERFLOW = int(os.getenv("DATABASE_MAX_OVERFLOW", 20))