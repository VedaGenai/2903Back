from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Float,
    Text,
    Boolean
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from app.database.connection import engine
from sqlalchemy.orm import registry
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from sqlalchemy.sql import func

mapper_registry = registry()
mapper_registry.configure()
Base = declarative_base()

# --- Admins Table ---
class Admin(Base):
    __tablename__ = "admins"
    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
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
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# --- Roles Table ---
class Role(Base):
    __tablename__ = "roles"
    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# --- Users Table ---
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    username = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.role_id"))
    organization_id = Column(Integer, ForeignKey("organizations.organization_id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    role = relationship("Role")
    organization = relationship("Organization")

# --- Subscription Plans Table ---
class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"
    plan_id = Column(Integer, primary_key=True, autoincrement=True)
    plan_name = Column(String, nullable=False)
    price_per_interview = Column(Float, nullable=False)
    max_interviews = Column(Integer, nullable=False)
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

    user = relationship("User")
    plan = relationship("SubscriptionPlan")

# --- Job Descriptions Table ---
class JobDescription(Base):
    __tablename__ = 'job_descriptions'

    job_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # Ensure this is not nullable
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    threshold_score = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class JobDescriptionCreate(BaseModel):
    title: str
    description: str
    threshold_score: float
    user_id: Optional[int] = None

class JobDescriptionResponse(BaseModel):
    job_id: int
    title: str
    description: str
    threshold_score: float
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class JobRequiredSkills(Base):
    __tablename__ = "job_required_skills"
    
    id = Column(Integer, primary_key=True)
    # Update to match the new primary key name
    job_id = Column(Integer, ForeignKey("job_descriptions.job_id"))
    
    job_description = relationship("JobDescription", back_populates="required_skills_relation")

# --- Skills Table ---
class Skill(Base):
    __tablename__ = "skills"
    skill_id = Column(Integer, primary_key=True, autoincrement=True)
    skill_name = Column(String, unique=True, nullable=False)

# --- Candidates Table ---
class Candidate(Base):
    __tablename__ = "candidates"
    
    candidate_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    resume_url = Column(String, nullable=False)
    # Update to match the new primary key name
    job_id = Column(Integer, ForeignKey("job_descriptions.job_id"))
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    job_description = relationship("JobDescription", back_populates="candidates")
    resumes = relationship("Resume", back_populates="candidate")

# --- Candidate Evaluations Table ---
class CandidateEvaluation(Base):
    __tablename__ = "candidate_evaluations"
    evaluation_id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, ForeignKey("candidates.candidate_id"), nullable=False)
    score = Column(Float, nullable=False)
    feedback = Column(Text, nullable=True)
    evaluation_date = Column(DateTime, default=datetime.utcnow)

    candidate = relationship("Candidate")

# --- Collaborators Table ---
class Collaborators(Base):
    __tablename__ = "collaborators"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    evaluation_id = Column(Integer, ForeignKey("candidate_evaluations.evaluation_id"), nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User")
    evaluation = relationship("CandidateEvaluation")

# --- Interviews Table ---
class Interview(Base):
    __tablename__ = "interviews"
    interview_id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, ForeignKey("candidates.candidate_id"), nullable=False)
    recruiter_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    status = Column(String(20), nullable=False)
    interview_date = Column(DateTime, nullable=False)
    feedback = Column(Text, nullable=True)

    candidate = relationship("Candidate")
    recruiter = relationship("User")

# --- Reports Table ---
class Report(Base):
    __tablename__ = "reports"
    report_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    report_type = Column(String, nullable=False)
    report_data = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")

# --- Notifications Table ---
class Notification(Base):
    __tablename__ = "notifications"
    notification_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    message = Column(String, nullable=False)
    read_status = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")

# --- Role Permissions Table ---
class RolePermission(Base):
    __tablename__ = "role_permissions"
    role_permission_id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)
    permission_name = Column(String, nullable=False)

    role = relationship("Role")

# --- Audit Trail Table ---
class AuditTrail(Base):
    __tablename__ = "audit_trails"
    audit_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    action = Column(String, nullable=False)
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")

# --- Discussions Table ---
class Discussion(Base):
    __tablename__ = "discussions"
    discussion_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    # Update to match the new primary key name
    job_id = Column(Integer, ForeignKey("job_descriptions.job_id"), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    job = relationship("JobDescription")

# --- Resumes Table ---
class Resume(Base):
    __tablename__ = "resumes"
    resume_id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey("candidates.candidate_id"))
    resume_url = Column(String, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    version = Column(Integer, nullable=False, default=1)
    parsed_data = Column(Text, nullable=True)

    # Relationships
    candidate = relationship("Candidate", back_populates="resumes")
    # --- Mapping all relationships ---
    recordings = relationship("Recording", back_populates="resume")
    evaluations = relationship("ResumeEvaluation", back_populates="resume")
    analytics = relationship("ResumeAnalytics",back_populates="resume",cascade="all, delete-orphan",lazy="joined")

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
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    resume = relationship("Resume", back_populates="evaluations")
    evaluator = relationship("User", foreign_keys=[evaluator_id])

# --- Resume Analytics Table ---
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
    generated_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    resume = relationship("Resume", back_populates="analytics")

# --- Threshold Scores Table ---
class ThresholdScore(Base):
    __tablename__ = "threshold_scores"
    threshold_id = Column(Integer, primary_key=True, autoincrement=True)
    # Update to match the new primary key name
    job_id = Column(Integer, ForeignKey("job_descriptions.job_id"), nullable=True)
    selection_score = Column(Float, nullable=False)
    rejection_score = Column(Float, nullable=False)
    threshold_value = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    job = relationship("JobDescription", foreign_keys=[job_id])

# --- Recordings Table ---
class Recording(Base):
    __tablename__ = "recordings"
    recording_id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey("resumes.resume_id"))
    # Update to match the new primary key name
    jd_id = Column(Integer, ForeignKey("job_descriptions.job_id"), nullable=True)
    speaker_type = Column(String, nullable=False)
    transcript_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    resume = relationship("Resume", back_populates="recordings")
    job_description = relationship("JobDescription", back_populates="recordings")

# Create all tables in the database
Base.metadata.create_all(bind=engine)
