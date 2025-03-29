# from pydantic_settings import BaseSettings
# from pathlib import Path
# from typing import Dict, Any
# import logging

# class Settings(BaseSettings):
#     BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
#     UPLOAD_DIR: Path = BASE_DIR / "uploads"
#     GOOGLE_API_KEY: str = "AIzaSyAWu-oajX5ufwmSCKlwYJyCtZZnW8MOfbg"
#     MODEL_NAME: str = "gemini-pro"
#     MODEL_TEMPERATURE: float = 0.2

#     MODEL_CONFIG: Dict[str, Any] = {
#         "name": MODEL_NAME,
#         "temperature": MODEL_TEMPERATURE
#     }

#     LOGGING_CONFIG: Dict[str, Any] = {
#         "level": "INFO",
#         "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
#     }

#     class Config:
#         env_file = "C:/Users/manis/Downloads/resume_thresholdbackend/fastHire99/backend/.env"

# settings = Settings()

# # Configure logger
# logger = logging.getLogger(__name__)
# logging.basicConfig(**settings.LOGGING_CONFIG)

# # Export all required constants
# UPLOAD_DIR = settings.UPLOAD_DIR
# GOOGLE_API_KEY = settings.GOOGLE_API_KEY
# MODEL_NAME = settings.MODEL_NAME
# MODEL_TEMPERATURE = settings.MODEL_TEMPERATURE
# MODEL_CONFIG = settings.MODEL_CONFIG
# LOGGING_CONFIG = settings.LOGGING_CONFIG

# # Create uploads directory
# UPLOAD_DIR.mkdir(exist_ok=True)


from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Dict, Any
import logging

class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    GOOGLE_API_KEY: str = "AIzaSyCD3RLN6AvkwebIwscPmPJEa6PbfdGy354"
    MODEL_NAME: str = "gemini-2.0-flash" 
    MODEL_TEMPERATURE: float = 0.2

    # JD Analysis Constants
    PERCENTAGE_TOLERANCE: float = 1.0
    MAX_RATING: float = 10.0
    
    MODEL_CONFIG: Dict[str, Any] = {
        "name": MODEL_NAME,
        "temperature": MODEL_TEMPERATURE
    }

    JD_ANALYSIS_CONFIG: Dict[str, Any] = {
        "percentage_tolerance": PERCENTAGE_TOLERANCE,
        "max_rating": MAX_RATING,
        "categories": {
            "skills": "Skill",
            "achievements_certifications": "Achievement/Certification",
            "skilled_activities": "Skilled Activity"
        }
    }

    LOGGING_CONFIG: Dict[str, Any] = {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    }

    db_user: str = Field(default='postgres')
    db_password: str = Field(default='Temp1234')
    db_host: str = Field(default='localhost')
    db_port: str = Field(default='5432')
    db_name: str = Field(default='fasthire99')
    class Config:
        env_file = "D:/projects/FH99-new-master/FH99-new-master/faas/backend/.env"

settings = Settings()

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(**settings.LOGGING_CONFIG)

# Export all required constants
UPLOAD_DIR = settings.UPLOAD_DIR
GOOGLE_API_KEY = settings.GOOGLE_API_KEY
MODEL_NAME = settings.MODEL_NAME
MODEL_TEMPERATURE = settings.MODEL_TEMPERATURE
MODEL_CONFIG = settings.MODEL_CONFIG
LOGGING_CONFIG = settings.LOGGING_CONFIG
JD_ANALYSIS_CONFIG = settings.JD_ANALYSIS_CONFIG
PERCENTAGE_TOLERANCE = settings.PERCENTAGE_TOLERANCE
MAX_RATING = settings.MAX_RATING

# Create uploads directory
UPLOAD_DIR.mkdir(exist_ok=True)
