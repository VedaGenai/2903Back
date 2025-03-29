from pydantic import BaseModel, EmailStr, ConfigDict
from sqlalchemy import Enum
from typing import List, Dict, Any, Optional, Union
from datetime import datetime


# User Models
class UserBase(BaseModel):
    """Base schema for user  """
    name: str
    email: str

# User Models
class UserResponse(BaseModel):
    name: str
    email: str
    role_id: Optional[int] = None
    user_id: int
    username: Optional[str] = None
    credentials: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=lambda string: string.replace('_', '')
    )


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    username: Optional[str] = None
    credentials: Dict[str, Any] = {}
    role_id: Optional[int] = None
    organization_id: Optional[int] = None


class RoleBase(BaseModel):
    """Base schema for role data"""
    role_name: str
    credentials: dict

class RoleCreate(BaseModel):
    name: str
    permissions: Dict[str, Any] = {}

class RoleResponse(BaseModel):
    role_id: int
    role_name: str
    permissions: Dict[str, Any] = {}
    
    class Config:
        orm_mode = True

# Department Enum
class DepartmentEnum(str, Enum):
    """Enum representing different departments"""
    HR = "HR"
    CLIENT = "CLIENT"
    RECRUITMENT = "RECRUITMENT"
    TECHNICAL = "TECHNICAL"
    ADMIN = "ADMIN"

# Organization Models
class OrganizationBase(BaseModel):
    """Base schema for organization data"""
    organization_name: str
    username: str
    email: str
    password: str

class OrganizationCreate(OrganizationBase):
    """Schema for creating a new organization"""
    password: str

class OrganizationResponse(OrganizationBase):
    """Schema for organization response data"""
    organization_id: int
    created_at: datetime
    updated_at: datetime
   
    model_config = ConfigDict(from_attributes=True)

class OrganizationUserResponse(BaseModel):
    """Schema for users in an organization"""
    user_id: int 
    name: str
    email: str
    username: str
    role_id: int
    role_name: str
    organization_id: int
    organization_name: str
   
    model_config = ConfigDict(from_attributes=True)
    prompt: Optional[str] = None

# Admin Models
class AdminCreate(BaseModel):
    """Schema for creating a new admin"""
    username: str
    email: EmailStr
    password: str
    mobile: str
    role: str = "ADMIN"  # Default value
    
class AdminResponse(BaseModel):
    """Schema for admin response data"""
    admin_id: int
    username: str
    email: str
    mobile: str
    department: str
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Authentication Models
class OTPRequest(BaseModel):
    """Schema for OTP request"""
    email: EmailStr
    mobile: str
    role: Optional[str] = None


class LoginRequest(BaseModel):
    """Schema for login request"""
    email: str
    password: str

class SkillData(BaseModel):
    importance: float
    selection_score: float
    rejection_score: float
    rating: float

class SkillCategory(BaseModel):
    skills: Dict[str, Dict[str, float]]
    achievements: Dict[str, Dict[str, float]]
    activities: Dict[str, Dict[str, float]]

class JobAnalysisResponse(BaseModel):
    roles: List[str]
    skills_data: Dict[str, SkillCategory]
    formatted_data: Dict[str, Any]
    selection_threshold: float
    rejection_threshold: float
    status: str
    raw_response: str
    data: Dict[str, Any]
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

class EvaluationResult(BaseModel):
    technical_score: int
    clarity_score: int
    completeness_score: int
    overall_score: int
    decision: str
    strengths: str
    improvements: str

class AudioTranscription(BaseModel):
    text: str
    clarity: str
    error: Optional[str] = None
    
class RoleSkills(BaseModel):
    skills: Dict[str, SkillData]
    
class RecordingRequest(BaseModel):
    source: str = "microphone"

class QAGenerateRequest(BaseModel):
    num_pairs: int
    original_qa: str

class QAEvaluateRequest(BaseModel):
    qa_text: str

class DashboardGenerationRequest(BaseModel):
    scale: int
    dashboard_index: int
    prompt: Optional[str] = None
    
class FeedbackCreate(BaseModel):
    candidate_id: int
    score: float
    feedback: str

class FeedbackResponse(BaseModel):
    evaluation_id: int
    candidate_id: int
    score: float
    feedback: str
    evaluation_date: datetime
    
class CandidateEvaluationResponse(BaseModel):
    evaluation_id: int
    candidate_id: int
    score: float
    feedback: Optional[str] = None
    evaluation_date: datetime
    
class QuestionResponseCreate(BaseModel):
    candidateId: int
    question: str
    response: str
    score: Optional[float] = None

class QuestionResponses(BaseModel):
    analytics_id: int
    resume_id: int
    ai_generated_question: str
    answer_text: str
    score: Optional[float] = None
    generated_at: datetime
    
class QuestionResponseSchema(BaseModel):
    analytics_id: int
    resume_id: int
    ai_generated_question: str
    answer_text: str
    score: Optional[float] = None
    generated_at: datetime