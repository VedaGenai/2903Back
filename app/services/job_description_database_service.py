from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Dict, List, Optional

from app.core.database import get_async_session
from app.models.job_description_model import JobDescriptionORMModel

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Dict, List, Optional
import json
import traceback

from app.core.database import get_async_session
from app.models.job_description_model import JobDescriptionORMModel

class JobDescriptionDatabaseService:
    def __init__(self, session: AsyncSession = None):
        """
        Initialize the database service with an async session
        
        :param session: Optional AsyncSession to use
        """
        self.session = session

    async def __aenter__(self):
        """
        Async context manager entry point
        """
        if not self.session:
            self.session_generator = get_async_session()
            self.session = await self.session_generator.__anext__()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """
        Async context manager exit point
        """
        if self.session:
            await self.session.close()

    def _sanitize_data(self, data):
        """
        Sanitize data to ensure it's JSON serializable
        """
        def convert(obj):
            try:
                json.dumps(obj)
                return obj
            except (TypeError, OverflowError):
                # If not directly serializable, convert to string
                return str(obj)
        
        if isinstance(data, dict):
            return {k: convert(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [convert(item) for item in data]
        return convert(data)

    async def create_job_description(
        self, 
        roles: List[str], 
        skills_data: Dict, 
        content: Optional[str] = None, 
        selection_threshold: Optional[float] = None, 
        rejection_threshold: Optional[float] = None,
        selected_prompts: Optional[List[str]] = None,
        raw_response: Optional[str] = None
    ) -> int:
        """
        Async method to insert a new job description into the database
        
        :return: Inserted job description ID
        """
        try:
            # Sanitize input data
            sanitized_roles = self._sanitize_data(roles)
            sanitized_skills_data = self._sanitize_data(skills_data)
            sanitized_selected_prompts = self._sanitize_data(selected_prompts)

            new_job_description = JobDescriptionORMModel(
                roles=sanitized_roles,
                skills_data=sanitized_skills_data,
                content=content,
                selection_threshold=selection_threshold,
                rejection_threshold=rejection_threshold,
                selected_prompts=sanitized_selected_prompts,
                status='success',
                raw_response=raw_response
            )
            
            self.session.add(new_job_description)
            await self.session.commit()
            await self.session.refresh(new_job_description)
            
            return new_job_description.id
        
        except Exception as e:
            await self.session.rollback()
            # Log the full traceback for debugging
            print(f"Error creating job description: {str(e)}")
            print(traceback.format_exc())
            raise e

    async def get_job_description_by_id(self, job_description_id: int):
        """
        Retrieve a job description by its ID
        
        :param job_description_id: ID of the job description
        :return: Job description object or None
        """
        result = await self.session.get(JobDescriptionORMModel, job_description_id)
        return result

    async def list_job_descriptions(self, limit: int = 100, offset: int = 0):
        """
        List job descriptions with optional pagination
        
        :param limit: Maximum number of records to return
        :param offset: Number of records to skip
        :return: List of job descriptions
        """
        query = select(JobDescriptionORMModel).offset(offset).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()