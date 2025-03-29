from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app1.database.session import Base

class JobAnalysis(Base):
    __tablename__ = 'job_analyses'

    id = Column(Integer, primary_key=True, index=True)
    roles = Column(JSON, nullable=False)
    skills_data = Column(JSON, nullable=False)
    content = Column(String)
    selection_threshold = Column(Float)
    rejection_threshold = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Optional: Relationship with individual skills
    individual_skills = relationship("IndividualSkill", back_populates="job_analysis")

class IndividualSkill(Base):
    __tablename__ = 'individual_skills'

    id = Column(Integer, primary_key=True, index=True)
    job_analysis_id = Column(Integer, ForeignKey('job_analyses.id'))
    role = Column(String)
    skill_name = Column(String)
    category = Column(String)  # skills, achievements, activities
    importance = Column(Float)
    selection_score = Column(Float)
    rejection_score = Column(Float)
    rating = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    job_analysis = relationship("JobAnalysis", back_populates="individual_skills")