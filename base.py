from sqlalchemy import (Column, Integer, String, ForeignKey, Enum, DateTime, Float, UniqueConstraint, Table, Text, create_engine)
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import datetime
import enum

# Database connection details
DATABASE_NAME = "fasthire99"
USERNAME = "postgres"  # Replace with your actual username
PASSWORD = "Temp1234"  # Replace with your actual password
HOST = "localhost"     # Adjust if your database is hosted elsewhere
PORT = "5432"          # Default PostgreSQL port, adjust if needed

# Create the SQLAlchemy engine with your database details
DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
engine = create_engine(DATABASE_URL)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base
Base = declarative_base()

# Admins Table
class Admin(Base):
    __tablename__ = "admins"
    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Users Table
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    username = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.role_id"))
    organization_id = Column(Integer, ForeignKey("organizations.organization_id"))
    
    role = relationship("Role")
    organization = relationship("Organization")

# Organizations Table
class Organization(Base):
    __tablename__ = "organizations"
    organization_id = Column(Integer, primary_key=True, autoincrement=True)
    organization_name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Roles Table
class Role(Base):
    __tablename__ = "roles"
    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# RolePermissions Table
class RolePermission(Base):
    __tablename__ = "role_permissions"
    role_permission_id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)
    permission_name = Column(String, nullable=False)

# SubscriptionPlans Table
class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"
    plan_id = Column(Integer, primary_key=True, autoincrement=True)
    plan_name = Column(String, nullable=False)
    price_per_interview = Column(Float, nullable=False)
    max_interviews = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Payments Table
class Payment(Base):
    __tablename__ = "payments"
    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("subscription_plans.plan_id"), nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow)
    amount_paid = Column(Float, nullable=False)
    status = Column(String(20), nullable=False)

# Interviews Table
class Interview(Base):
    __tablename__ = "interviews"
    interview_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    job_id = Column(Integer, ForeignKey("job_descriptions.job_id"), nullable=False)
    recruiter_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# JobDescriptions Table
class JobDescription(Base):
    __tablename__ = "job_descriptions"
    job_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    threshold_score = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# JobRequiredSkills Table (Many-to-Many Relationship)
class JobRequiredSkill(Base):
    __tablename__ = "job_required_skills"
    job_id = Column(Integer, ForeignKey("job_descriptions.job_id"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.skill_id"), primary_key=True)

# Skills Table
class Skill(Base):
    __tablename__ = "skills"
    skill_id = Column(Integer, primary_key=True, autoincrement=True)
    skill_name = Column(String, unique=True, nullable=False)

# Candidates Table
class Candidate(Base):
    __tablename__ = "candidates"
    candidate_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    resume_url = Column(String, nullable=False)
    job_id = Column(Integer, ForeignKey("job_descriptions.job_id"), nullable=False)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# CandidateEvaluations Table
class CandidateEvaluation(Base):
    __tablename__ = "candidate_evaluations"
    evaluation_id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, ForeignKey("candidates.candidate_id"), nullable=False)
    score = Column(Float, nullable=False)
    feedback = Column(String, nullable=False)

# Reports Table
class Report(Base):
    __tablename__ = "reports"
    report_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    report_type = Column(String, nullable=False)
    report_data = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Notifications Table
class Notification(Base):
    __tablename__ = "notifications"
    notification_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    message = Column(String, nullable=False)
    read_status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Function to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all tables in the database
def init_db():
    Base.metadata.create_all(bind=engine)

# If this file is run directly, initialize the database
if __name__ == "__main__":
    init_db()
