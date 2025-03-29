from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.base import JobDescription
from datetime import datetime
from typing import Dict, Any

class DatabaseService:
    def __init__(self, db: Session):
        self.db = db

    def create_job_description(self, job_description_data: Dict[str, Any]):
        try:
            # If no user_id is provided, use a default
            if 'user_id' not in job_description_data or job_description_data['user_id'] is None:
                job_description_data['user_id'] = 1  # Default user ID

            # Create job description instance
            job_description = JobDescription(**job_description_data)
            
            # Add and commit
            self.db.add(job_description)
            self.db.commit()
            self.db.refresh(job_description)
            
            return job_description
        
        except IntegrityError as e:
            self.db.rollback()
            raise e
        except Exception as e:
            self.db.rollback()
            raise e