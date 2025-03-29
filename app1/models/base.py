from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Float,
    Text,
    Boolean,
    JSON
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from sqlalchemy.orm import registry

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import logging

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Dict, Any, Optional
from sqlalchemy import Column, Integer, String, JSON, Float, Text, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
from sqlalchemy.types import TypeDecorator, String as SqlaString
import json

Base = declarative_base()
class JSONEncodedDict(TypeDecorator):
    """Enables JSON storage by encoding and decoding Python dictionaries."""
    impl = SqlaString

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return json.loads(value)

class JobAnalysis(Base):
    __tablename__ = "job_analyses"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    roles = Column(JSONEncodedDict, nullable=False)
    skills_data = Column(JSONEncodedDict, nullable=False)
    content = Column(Text, nullable=True)
    selection_threshold = Column(Float, nullable=False)
    rejection_threshold = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<JobAnalysis(id={self.id}, roles={self.roles})>"
    
class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    
    # Database settings
    db_user: str = Field(default='postgres')
    db_password: str = Field(default='Temp1234')
    db_host: str = Field(default='localhost')
    db_port: str = Field(default='5432')
    db_name: str = Field(default='fasthire')
    
    # Add the new fields that were causing errors
    database_url: Optional[str] = None
    database_pool_size: Optional[str] = "10"
    database_max_overflow: Optional[str] = "20"
    
    # API settings
    GOOGLE_API_KEY: str = "AIzaSyCD3RLN6AvkwebIwscPmPJEa6PbfdGy354"
    api_key: Optional[str] = None  # Add the api_key field
    
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
    
    class Config:
        # Use a relative path for the .env file
        env_file = Path(__file__).resolve().parent.parent.parent / ".env"
        # Allow extra fields from .env file
        extra = "ignore"  # This will ignore extra fields instead of raising errors

settings = Settings()

# Configure logging
logger = logging.getLogger(__name__)

# Use the database_url from .env if provided, otherwise construct it from components
DATABASE_URL = settings.database_url or f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

# Add pool_pre_ping=True for connection health checks
engine = create_engine(
    DATABASE_URL, 
    pool_pre_ping=True,  # Test connections before using them
    pool_recycle=3600,   # Recycle connections after 1 hour
    pool_size=int(settings.database_pool_size),  # Use the pool size from settings
    max_overflow=int(settings.database_max_overflow),  # Use max overflow from settings
    echo=False           # Set to True for SQL logging during development
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Use the updated import from sqlalchemy.orm
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database operation error: {e}", exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()

mapper_registry = registry()
mapper_registry.configure()
Base = declarative_base()

# --- Admins Table (kept separate for enterprise security) ---
class Admin(Base):
    __tablename__ = "admins"
    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    activity_type = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# --- Organizations Table ---
class Organization(Base):
    __tablename__ = "organizations"
    organization_id = Column(Integer, primary_key=True, autoincrement=True)
    organization_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    activity_type = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# --- ATS Integration Table (kept separate for enterprise integration) ---
class ATSIntegration(Base):
    __tablename__ = "ats_integration"
    integration_id = Column(Integer, primary_key=True, autoincrement=True)
    organization_id = Column(Integer, ForeignKey("organizations.organization_id"))
    organization_name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    job_descriptions = Column(JSON, nullable=False)
    resumes = Column(JSON, nullable=False)
    activity_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    organization = relationship("Organization")
    user = relationship("User")

# --- Roles Table ---
class Role(Base):
    __tablename__ = "roles"
    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String, nullable=False)
    activity_type = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# --- Role Permissions Table (kept separate for enterprise access control) ---
class RolePermission(Base):
    __tablename__ = "role_permissions"
    role_permission_id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)
    permission_name = Column(String, nullable=False)
    activity_type = Column(String, nullable=True)
    
    role = relationship("Role")

# --- Users Table ---
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    username = Column(String, nullable=False)
    role = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.role_id"))
    organization_id = Column(Integer, ForeignKey("organizations.organization_id"))
    activity_type = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    role_relation = relationship("Role")
    organization = relationship("Organization")

# --- Subscription Plans Table ---
class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"
    plan_id = Column(Integer, primary_key=True, autoincrement=True)
    plan_name = Column(String, nullable=False)
    price_per_interview = Column(Float, nullable=False)
    max_interviews = Column(Integer, nullable=False)
    activity_type = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# --- Payments Table ---
class Payment(Base):
    __tablename__ = "payments"
    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("subscription_plans.plan_id"), nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow)
    amount_paid = Column(Float, nullable=False)
    status = Column(String(20), nullable=False)
    activity_type = Column(String, nullable=True)
    
    user = relationship("User")
    plan = relationship("SubscriptionPlan")

# --- Job Descriptions Table ---
class JobDescription(Base):
    __tablename__ = "job_descriptions"
    job_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    raw_text = Column(Text, nullable=True)
    source_file = Column(String, nullable=True)
    keywords = Column(Text, nullable=True)
    status = Column(String, nullable=True)
    department = Column(String, nullable=True)
    required_skills = Column(Text, nullable=True)
    experience_level = Column(String, nullable=True)
    education_requirements = Column(String, nullable=True)
    threshold_score = Column(Float, nullable=False)
    activity_type = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    recordings = relationship("Recording", back_populates="job_description")
    required_skills_relation = relationship("JobRequiredSkills", back_populates="job_description")
    candidates = relationship("Candidate", back_populates="job_description")

# --- Job Required Skills Table ---
class JobRequiredSkills(Base):
    __tablename__ = "job_required_skills"
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("job_descriptions.job_id"))
    skill_id = Column(Integer, ForeignKey("skills.skill_id"))
    importance = Column(Float, nullable=True)
    selection_weight = Column(Float, nullable=True)
    rejection_weight = Column(Float, nullable=True)
    activity_type = Column(String, nullable=True)
    
    job_description = relationship("JobDescription", back_populates="required_skills_relation")
    skill = relationship("Skill")

# --- Skills Table (kept separate for enterprise skill management) ---
class Skill(Base):
    __tablename__ = "skills"
    skill_id = Column(Integer, primary_key=True, autoincrement=True)
    skill_name = Column(String, unique=True, nullable=False)
    skill_type = Column(String, nullable=True)  # Technical, Soft, Domain
    activity_type = Column(String, nullable=True)

# --- Candidates Table ---
class Candidate(Base):
    __tablename__ = "candidates"
    candidate_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    resume_url = Column(String, nullable=False)
    job_id = Column(Integer, ForeignKey("job_descriptions.job_id"))
    status = Column(String(20), nullable=False)
    activity_type = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    job_description = relationship("JobDescription", back_populates="candidates")
    resumes = relationship("Resume", back_populates="candidate")

# --- Candidate Evaluations Table ---
class CandidateEvaluation(Base):
    __tablename__ = "candidate_evaluations"
    evaluation_id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, ForeignKey("candidates.candidate_id"), nullable=False)
    job_id = Column(Integer, ForeignKey("job_descriptions.job_id"), nullable=False)
    interview_id = Column(Integer, ForeignKey("interviews.interview_id"), nullable=True)
    score = Column(Float, nullable=False)
    feedback = Column(Text, nullable=True)
    strengths = Column(Text, nullable=True)
    weaknesses = Column(Text, nullable=True)
    recommendation = Column(String, nullable=True)
    evaluation_type = Column(String, nullable=False, default="automated")
    activity_type = Column(String, nullable=True)
    evaluation_date = Column(DateTime, default=datetime.utcnow)
    
    candidate = relationship("Candidate")
    job = relationship("JobDescription")
    interview = relationship("Interview")

# --- Collaborators Table ---
class Collaborators(Base):
    __tablename__ = "collaborators"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    evaluation_id = Column(Integer, ForeignKey("candidate_evaluations.evaluation_id"), nullable=False)
    role = Column(String, nullable=False)
    activity_type = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User")
    evaluation = relationship("CandidateEvaluation")

# --- Interviews Table ---
class Interview(Base):
    __tablename__ = "interviews"
    interview_id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, ForeignKey("candidates.candidate_id"), nullable=False)
    job_id = Column(Integer, ForeignKey("job_descriptions.job_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    interview_score = Column(Integer, nullable=False)
    interview_date = Column(DateTime, nullable=False)
    feedback = Column(JSON, nullable=True)
    status = Column(String(20), nullable=False, default="Scheduled")
    activity_type = Column(String, nullable=True)
    
    candidate = relationship("Candidate")
    job = relationship("JobDescription")
    user = relationship("User")

# --- Reports Table (kept separate for enterprise reporting) ---
class Report(Base):
    __tablename__ = "reports"
    report_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    report_type = Column(String, nullable=False)
    report_data = Column(Text, nullable=False)
    activity_type = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User")

# --- Notifications Table ---
class NotificationandAllerts(Base):
    __tablename__ = "notifications_and_alerts"
    notification_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    message = Column(String, nullable=False)
    read_status = Column(Boolean, default=False)
    activity_type = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User")

# --- Audit Trail Table (kept separate for enterprise compliance) ---
class AuditTrail(Base):
    __tablename__ = "audit_trails"
    audit_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    action = Column(String, nullable=False)
    details = Column(Text, nullable=True)
    activity_type = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User")

# --- Discussions Table ---
class Discussion(Base):
    __tablename__ = "discussions"
    discussion_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    job_id = Column(Integer, ForeignKey("job_descriptions.job_id"), nullable=False)
    message = Column(Text, nullable=False)
    activity_type = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User")
    job = relationship("JobDescription")

# --- Resumes Table ---
class Resume(Base):
    __tablename__ = "resumes"
    resume_id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("job_descriptions.job_id"))
    candidate_id = Column(Integer, ForeignKey("candidates.candidate_id"))
    resume_url = Column(String, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    version = Column(Integer, nullable=False, default=1)
    parsed_data = Column(Text, nullable=True)
    activity_type = Column(String, nullable=True)
    
    # Relationships
    candidate = relationship("Candidate", back_populates="resumes")
    recordings = relationship("Recording", back_populates="resume")
    evaluations = relationship("ResumeEvaluation", back_populates="resume")
    analytics = relationship("ResumeAnalytics", back_populates="resume", cascade="all, delete-orphan", lazy="joined")

# --- Resume Evaluation Table ---
class ResumeEvaluation(Base):
    __tablename__ = "resume_evaluations"
    evaluation_id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey("resumes.resume_id"))
    evaluator_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    score = Column(Float, nullable=True)
    strengths = Column(Text, nullable=True)
    weaknesses = Column(Text, nullable=True)
    feedback = Column(Text, nullable=True)
    evaluation_type = Column(String, nullable=False, default="automated")
    activity_type = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    resume = relationship("Resume", back_populates="evaluations")
    evaluator = relationship("User", foreign_keys=[evaluator_id])

# --- Resume Analytics Table (kept separate for enterprise analytics) ---
class ResumeAnalytics(Base):
    __tablename__ = "resume_analytics"
    analytics_id = Column(Integer, primary_key=True, autoincrement=True)
    resume_id = Column(Integer, ForeignKey("resumes.resume_id"), nullable=False)
    ai_generated_question = Column(String, nullable=False)
    answer_text = Column(Text, nullable=True)
    score = Column(Float, nullable=True)
    strengths = Column(Text, nullable=True)
    weaknesses = Column(Text, nullable=True)
    insights = Column(Text, nullable=True)
    activity_type = Column(String, nullable=True)
    generated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    resume = relationship("Resume", back_populates="analytics")

# --- Threshold Scores Table ---
class ThresholdScore(Base):
    __tablename__ = "threshold_scores"
    threshold_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    job_id = Column(Integer, ForeignKey("job_descriptions.job_id"), nullable=True)
    selection_score = Column(Float, nullable=False)
    rejection_score = Column(Float, nullable=False)
    threshold_value = Column(Float, nullable=False)
    threshold_result = Column(JSON, nullable=True)
    threshold_prompts = Column(Text, nullable=True)
    custom_prompts = Column(Text, nullable=True)
    sample_prompts_history = Column(Text, nullable=True)
    activity_type = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    threshold_history = Column(JSON, nullable=True)

    job = relationship("JobDescription", foreign_keys=[job_id])
    user = relationship("User", foreign_keys=[user_id])
    
# --- User Feedback Table ---
class UserFeedback(Base):
    __tablename__ = "user_feedback"
    feedback_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    feedback_type = Column(String, nullable=False)  # Bug, Feature Request, General
    feedback_text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=True)  # 1-5 star rating
    status = Column(String, nullable=False, default="Pending")  # Pending, In Progress, Resolved
    activity_type = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User")

# --- Recordings Table ---
class Recording(Base):
    __tablename__ = "recordings"
    recording_id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey("resumes.resume_id"))
    jd_id = Column(Integer, ForeignKey("job_descriptions.job_id"), nullable=True)
    speaker_type = Column(String, nullable=False)
    transcript_text = Column(Text, nullable=False)
    interviewer_text = Column(Text, nullable=True)
    candidate_text = Column(Text, nullable=True)
    status = Column(String, nullable=True)
    activity_type = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    resume = relationship("Resume", back_populates="recordings")
    job_description = relationship("JobDescription", back_populates="recordings")



# Create all tables in the database
Base.metadata.create_all(bind=engine)
