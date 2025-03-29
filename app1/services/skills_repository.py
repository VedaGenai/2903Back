from sqlalchemy.orm import Session
from app1.models.base import JobAnalysis  # Import the new model
import json
from typing import List, Dict
from datetime import datetime

class SkillsRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_job_analysis(
        self, 
        roles: List[str], 
        skills_data: Dict, 
        content: str, 
        selection_threshold: float, 
        rejection_threshold: float
    ):
        """
        Save job analysis data to the database
        
        Args:
            roles: List of roles identified in the job description
            skills_data: Detailed skills data dictionary
            content: Raw LLM response content
            selection_threshold: Calculated selection threshold
            rejection_threshold: Calculated rejection threshold
        
        Returns:
            Saved JobAnalysis instance
        """
        try:
            # Ensure roles and skills_data are properly serialized JSON strings
            roles_json = json.dumps(roles) if not isinstance(roles, str) else roles
            skills_data_json = json.dumps(skills_data) if not isinstance(skills_data, str) else skills_data
            
            # Create job analysis entry
            job_analysis = JobAnalysis(
                roles=roles_json,
                skills_data=skills_data_json,
                content=content,
                selection_threshold=selection_threshold,
                rejection_threshold=rejection_threshold,
                created_at=datetime.utcnow()
            )
            
            self.db.add(job_analysis)
            self.db.commit()
            self.db.refresh(job_analysis)
            
            return job_analysis
        
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Failed to save job analysis: {str(e)}")
        
def get_job_analysis_by_id(self, analysis_id: int) -> JobAnalysis:
        """
        Retrieve a job analysis by its ID.
        
        Args:
            analysis_id: The ID of the job analysis to retrieve
            
        Returns:
            The JobAnalysis object if found, None otherwise
        """
        return self.db.query(JobAnalysis).filter(JobAnalysis.id == analysis_id).first()

    # Add this method to your SkillsRepository class
def get_all_job_analyses(self, skip=0, limit=None, role_filter=None):
    """
    Retrieve all job analyses from the database with optional filtering and pagination.
    
    Args:
        skip (int): Number of records to skip (for pagination)
        limit (int): Maximum number of records to return (for pagination)
        role_filter (str): Filter analyses by role name
        
    Returns:
        list: List of JobAnalysis objects
    """
    from app1.models.skill_model import JobAnalysis
    
    query = self.db.query(JobAnalysis)
    
    if role_filter:
        query = query.filter(JobAnalysis.roles.like(f'%{role_filter}%'))
    
    if skip:
        query = query.offset(skip)
    
    if limit:
        query = query.limit(limit)
    
    return query.all()