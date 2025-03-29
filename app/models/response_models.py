from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Union

class SkillData(BaseModel):
    importance: float
    selection_score: float
    rejection_score: float
    rating: float

class JobAnalysisResponse(BaseModel):
    roles: List[str]
    skills_data: Dict[str, Any]
    formatted_data: Dict[str, Any]
    selection_threshold: float
    rejection_threshold: float
    status: str
    raw_response: str
    selected_prompts: str

class DashboardResponse(BaseModel):
    status: str
    message: str
    dashboards: List[Dict[str, Any]]
    selection_threshold: float
    rejection_threshold: float
    number_of_dashboards: int

class ErrorResponse(BaseModel):
    status: str
    message: str

class AnalysisResult(BaseModel):
    success: bool
    data: Union[JobAnalysisResponse, ErrorResponse]
