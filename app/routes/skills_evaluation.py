from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.services.llm_service import LLMService
from app.services.dashboard_service import DashboardService
from app1.services.skills_repository import SkillsRepository
from app1.database.session import get_db
from app.utils.helpers import process_pdf
from app.models.response_models import JobAnalysisResponse
from app1.database.initialization import init_db  # Import the new initialization function
import logging
import json
from typing import List, Dict, Any
from sqlalchemy import inspection

# Initialize database when the module is imported
try:
    # Optional: You can pass custom parameters if needed
    init_db()
    logging.info("Database initialized successfully in skills_evaluation")
except Exception as e:
    logging.error(f"Database initialization failed: {e}")

analyze_job_description_router = APIRouter()
logger = logging.getLogger(__name__)

@analyze_job_description_router.post("/analyze_job_description/", response_model=JobAnalysisResponse)
async def analyze_job_description(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    try:
        text = await process_pdf(file)
        llm_service = LLMService()
        roles, skills_data, content, thresholds, selected_prompts = await llm_service.process_job_description(text)
        
        selection_threshold, rejection_threshold = thresholds
        
        # Create repository with database session
        skills_repo = SkillsRepository(db)
        
        
        # Save to database
        saved_analysis = skills_repo.save_job_analysis(
            roles=roles,
            skills_data=skills_data,
            content=content,
            selection_threshold=selection_threshold,
            rejection_threshold=rejection_threshold
        )

        response_dict = {
            "roles": roles,
            "skills_data": skills_data,
            "content": content,
            "analysis": {
                "role": roles[0] if roles else "",
                "skills": skills_data
            },
            "database_id": saved_analysis.id
        }

        return JobAnalysisResponse(
            roles=roles,
            skills_data=skills_data,
            formatted_data=response_dict,
            selection_threshold=selection_threshold,
            rejection_threshold=rejection_threshold,
            status="success",
            raw_response=content,
            selected_prompts=selected_prompts,
            database_id=saved_analysis.id
        )
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@analyze_job_description_router.get("/analyze_job_description/{analysis_id}", response_model=JobAnalysisResponse)
async def get_job_description_analysis(
    analysis_id: int, 
    db: Session = Depends(get_db)
):
    try:
        # Create repository with database session
        skills_repo = SkillsRepository(db)
        
        # Query directly from the database model if repository method is missing
        from app1.models.skill_model import JobAnalysis
        analysis = db.query(JobAnalysis).filter(JobAnalysis.id == analysis_id).first()
        
        if not analysis:
            raise HTTPException(status_code=404, detail=f"Job analysis with ID {analysis_id} not found")
        
        # Parse JSON strings back to Python objects
        roles = json.loads(analysis.roles) if isinstance(analysis.roles, str) else analysis.roles
        skills_data = json.loads(analysis.skills_data) if isinstance(analysis.skills_data, str) else analysis.skills_data
        
        # Construct the response using the retrieved data
        response_dict = {
            "roles": roles,
            "skills_data": skills_data,
            "content": analysis.content,
            "analysis": {
                "role": roles[0] if roles else "",
                "skills": skills_data
            },
            "database_id": analysis.id
        }
        
        # Default to empty string for selected_prompts if it's not available
        selected_prompts = "" if not hasattr(analysis, "selected_prompts") else analysis.selected_prompts
        
        return JobAnalysisResponse(
            roles=roles,
            skills_data=skills_data,
            formatted_data=response_dict,
            selection_threshold=analysis.selection_threshold,
            rejection_threshold=analysis.rejection_threshold,
            status="success",
            raw_response=analysis.content,
            selected_prompts=selected_prompts,
            database_id=analysis.id
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving job analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    

@analyze_job_description_router.get("/job_analyses_repo/", response_model=List[JobAnalysisResponse])
async def get_all_job_analyses_using_repo(
    skip: int = 0, 
    limit: int = 100,
    role_filter: str = None,
    db: Session = Depends(get_db)
):
    try:
        # Create repository with database session
        skills_repo = SkillsRepository(db)
        
        # Get all analyses using the repository method
        analyses = skills_repo.get_all_job_analyses(skip=skip, limit=limit, role_filter=role_filter)
        
        if not analyses:
            return []
        
        response_list = []
        
        for analysis in analyses:
            # Parse JSON strings back to Python objects
            roles = json.loads(analysis.roles) if isinstance(analysis.roles, str) else analysis.roles
            skills_data = json.loads(analysis.skills_data) if isinstance(analysis.skills_data, str) else analysis.skills_data
            
            response_dict = {
                "roles": roles,
                "skills_data": skills_data,
                "content": analysis.content,
                "analysis": {
                    "role": roles[0] if roles else "",
                    "skills": skills_data
                },
                "database_id": analysis.id
            }
            
            selected_prompts = "" if not hasattr(analysis, "selected_prompts") else analysis.selected_prompts
            
            response = JobAnalysisResponse(
                roles=roles,
                skills_data=skills_data,
                formatted_data=response_dict,
                selection_threshold=analysis.selection_threshold,
                rejection_threshold=analysis.rejection_threshold,
                status="success",
                raw_response=analysis.content,
                selected_prompts=selected_prompts,
                database_id=analysis.id
            )
            
            response_list.append(response)
        
        return response_list
    
    except Exception as e:
        logger.error(f"Error retrieving all job analyses: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@analyze_job_description_router.get("/job_analyses_paginated/", response_model=List[JobAnalysisResponse])
async def get_paginated_job_analyses(
    skip: int = 0, 
    limit: int = 10,
    role_filter: str = None,
    db: Session = Depends(get_db)
):
    try:
        from app1.models.skill_model import JobAnalysis
        
        # Start with a base query
        query = db.query(JobAnalysis)
        
        # Apply filters if provided
        if role_filter:
            # This will work if 'roles' is stored as a JSON string containing the role
            query = query.filter(JobAnalysis.roles.like(f'%{role_filter}%'))
        
        # Apply pagination and execute query
        analyses = query.offset(skip).limit(limit).all()
        
        if not analyses:
            return []
        
        response_list = []
        
        for analysis in analyses:
            # Parse JSON strings back to Python objects
            roles = json.loads(analysis.roles) if isinstance(analysis.roles, str) else analysis.roles
            skills_data = json.loads(analysis.skills_data) if isinstance(analysis.skills_data, str) else analysis.skills_data
            
            response_dict = {
                "roles": roles,
                "skills_data": skills_data,
                "content": analysis.content,
                "analysis": {
                    "role": roles[0] if roles else "",
                    "skills": skills_data
                },
                "database_id": analysis.id
            }
            
            selected_prompts = "" if not hasattr(analysis, "selected_prompts") else analysis.selected_prompts
            
            response = JobAnalysisResponse(
                roles=roles,
                skills_data=skills_data,
                formatted_data=response_dict,
                selection_threshold=analysis.selection_threshold,
                rejection_threshold=analysis.rejection_threshold,
                status="success",
                raw_response=analysis.content,
                selected_prompts=selected_prompts,
                database_id=analysis.id
            )
            
            response_list.append(response)
        
        return response_list
    
    except Exception as e:
        logger.error(f"Error retrieving paginated job analyses: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
from typing import List

@analyze_job_description_router.get("/job_analyses/", response_model=List[JobAnalysisResponse])
async def get_all_job_analyses(db: Session = Depends(get_db)):
    try:
        # Import the JobAnalysis model
        from app1.models.skill_model import JobAnalysis
        
        # Query all records from the database
        analyses = db.query(JobAnalysis).all()
        
        if not analyses:
            return []
        
        # Create a list to store the responses
        response_list = []
        
        # Convert each database record to a response model
        for analysis in analyses:
            # Parse JSON strings back to Python objects
            roles = json.loads(analysis.roles) if isinstance(analysis.roles, str) else analysis.roles
            skills_data = json.loads(analysis.skills_data) if isinstance(analysis.skills_data, str) else analysis.skills_data
            
            # Construct the response dict
            response_dict = {
                "roles": roles,
                "skills_data": skills_data,
                "content": analysis.content,
                "analysis": {
                    "role": roles[0] if roles else "",
                    "skills": skills_data
                },
                "database_id": analysis.id
            }
            
            # Default to empty string for selected_prompts if it's not available
            selected_prompts = "" if not hasattr(analysis, "selected_prompts") else analysis.selected_prompts
            
            # Create response object
            response = JobAnalysisResponse(
                roles=roles,
                skills_data=skills_data,
                formatted_data=response_dict,
                selection_threshold=analysis.selection_threshold,
                rejection_threshold=analysis.rejection_threshold,
                status="success",
                raw_response=analysis.content,
                selected_prompts=selected_prompts,
                database_id=analysis.id
            )
            response_list.append(response)
        return response_list
    except Exception as e:
        logger.error(f"Error retrieving all job analyses: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))