# # from app.models.user import Base, engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import create_engine
# from datetime import datetime
# from sqlalchemy import Column, Integer, String

# Base = declarative_base
# engine = create_engine('your_database_connection_string_here')


# from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime, Text, Numeric, CheckConstraint
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func
# from sqlalchemy.dialects.postgresql import JSONB
# from typing import List, Dict, Any, Optional

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     email = Column(String, unique=True, index=True)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     # Add other user fields as needed

# class Roles(Base):
#     __tablename__ = "roles"
#     roleid = Column(Integer, primary_key=True)
#     rolename = Column(String(50), unique=True, nullable=False)
    
#     # Relationships
#     users = relationship("User", back_populates="role")

# class SubscriptionPlans(Base):
#     __tablename__ = "subscriptionplans"
#     planid = Column(Integer, primary_key=True)
#     planname = Column(String(100), nullable=False)
#     priceperinterview = Column(Numeric(10, 2), nullable=False)
#     maxinterviews = Column(Integer)
#     createdat = Column(DateTime, server_default=func.now())
    
#     # Relationships
#     payments = relationship("Payments", back_populates="plan")

# class Payments(Base):
#     __tablename__ = "payments"
#     paymentid = Column(Integer, primary_key=True)
#     userid = Column(Integer, ForeignKey('users.userid'))
#     planid = Column(Integer, ForeignKey('subscriptionplans.planid'))
#     paymentdate = Column(DateTime, server_default=func.now())
#     amountpaid = Column(Numeric(10, 2), nullable=False)
#     status = Column(String(50), CheckConstraint("status IN ('Success', 'Failed', 'Pending')"))
    
#     # Relationships
#     user = relationship("User")
#     plan = relationship("SubscriptionPlans", back_populates="payments")

# class JobDescriptions(Base):
#     __tablename__ = "jobdescriptions"
#     jdid = Column(Integer, primary_key=True)
#     userid = Column(Integer, ForeignKey('users.userid'))
#     title = Column(String(150), nullable=False)
#     description = Column(Text, nullable=False)
#     thresholdscore = Column(Integer, nullable=False)
#     createdat = Column(DateTime, server_default=func.now())
#     updatedat = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
#     # Relationships
#     user = relationship("User")
#     interviews = relationship("Interviews", back_populates="job_description")

# class Interviews(Base):
#     __tablename__ = "interviews"
#     interviewid = Column(Integer, primary_key=True)
#     jdid = Column(Integer, ForeignKey('jobdescriptions.jdid'))
#     recruiterid = Column(Integer, ForeignKey('users.userid'))
#     candidatename = Column(String(100))
#     candidateemail = Column(String(150))
#     status = Column(String(50), CheckConstraint("status IN ('Pending', 'Completed', 'Rejected')"))
#     createdat = Column(DateTime, server_default=func.now())
    
#     # Relationships
#     job_description = relationship("JobDescriptions", back_populates="interviews")
#     recruiter = relationship("User", back_populates="interviews")
#     questions = relationship("Questions", back_populates="interview")
#     evaluations = relationship("Evaluations", back_populates="interview")

# class Questions(Base):
#     __tablename__ = "questions"
#     questionid = Column(Integer, primary_key=True)
#     interviewid = Column(Integer, ForeignKey('interviews.interviewid'))
#     questiontext = Column(Text, nullable=False)
#     generatedby = Column(String(50), CheckConstraint("generatedby IN ('Recruiter', 'AI')"))
#     createdat = Column(DateTime, server_default=func.now())
    
#     # Relationships
#     interview = relationship("Interviews", back_populates="questions")
#     candidate_responses = relationship("CandidateResponses", back_populates="question")

# class CandidateResponses(Base):
#     __tablename__ = "candidateresponses"
#     responseid = Column(Integer, primary_key=True)
#     questionid = Column(Integer, ForeignKey('questions.questionid'))
#     candidateanswer = Column(Text, nullable=False)
#     evaluatedscore = Column(Numeric(5, 2))
#     mappedaianswer = Column(Text, nullable=False)
#     createdat = Column(DateTime, server_default=func.now())
    
#     # Relationships
#     question = relationship("Questions", back_populates="candidate_responses")

# class Skills(Base):
#     __tablename__ = "skills"
#     skillid = Column(Integer, primary_key=True)
#     skillname = Column(String(100), unique=True, nullable=False)
    
#     # Relationships
#     evaluations = relationship("Evaluations", back_populates="skill")

# class Evaluations(Base):
#     __tablename__ = "evaluations"
#     evaluationid = Column(Integer, primary_key=True)
#     interviewid = Column(Integer, ForeignKey('interviews.interviewid'))
#     skillid = Column(Integer, ForeignKey('skills.skillid'))
#     score = Column(Numeric(5, 2))
#     comments = Column(Text)
#     createdat = Column(DateTime, server_default=func.now())
    
#     # Relationships
#     interview = relationship("Interviews", back_populates="evaluations")
#     skill = relationship("Skills", back_populates="evaluations")

# class Reports(Base):
#     __tablename__ = "reports"
#     reportid = Column(Integer, primary_key=True)
#     userid = Column(Integer, ForeignKey('users.userid'))
#     reporttype = Column(String(50), nullable=False)
#     reportdata = Column(JSONB, nullable=False)
#     createdat = Column(DateTime, server_default=func.now())
    
#     # Relationships
#     user = relationship("User", back_populates="reports")

# class ExternalIntegrations(Base):
#     __tablename__ = "externalintegrations"
#     integrationid = Column(Integer, primary_key=True)
#     organizationname = Column(String(100))
#     integrationtype = Column(String(50), CheckConstraint("integrationtype IN ('HR Database', 'Social Media')"))
#     connectiondetails = Column(JSONB, nullable=False)
#     createdat = Column(DateTime, server_default=func.now())

# class SkillWeightage(Base):
#     importance: float
#     selection_score: float
#     rejection_score: float

# class RoleSkills(Base):
#     skills: Dict[str, SkillWeightage]

# class JobAnalysisResponse(Base):
#     roles: dict[str]
#     skills_data: dict[str, Dict[str, SkillWeightage]]
#     data: dict[str, Any]

# class DashboardResponse(Base):
#     status: str
#     message: str
#     dashboards: List[Any]
#     selection_threshold: float
#     rejection_threshold: float
#     number_of_dashboards: int = 1


# # Create all tables in the database
# Base.metadata.create_all(bind=engine)