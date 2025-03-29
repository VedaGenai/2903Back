import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey, Enum, func, JSON, CheckConstraint
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, validates
from sqlalchemy.ext.declarative import declarative_base
import enum
import pandas as pd
import logging
import json
from datetime import datetime
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from fastapi import APIRouter
 
router = APIRouter()


# Configure password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Enhanced logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def create_fasthire_frdb():
    # Connect to PostgreSQL server
    conn = psycopg2.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"), 
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    # Create a cursor
    cursor = conn.cursor()
    
    # Create database
    try:
        cursor.execute("CREATE DATABASE fasthire_frdb")
        print("Database 'fasthire_frdb' created successfully")
    except psycopg2.Error as e:
        print(f"Database creation response: {e}")
    finally:
        # Close cursor and connection
        cursor.close()
        conn.close()

# Enum definitions
class CandidateStatus(enum.Enum):
    Applied = 'Applied'
    Screening = 'Screening'
    Interview = 'Interview'
    Selected = 'Selected'
    Rejected = 'Rejected'
    Onboarding = 'Onboarding'
    Joined = 'Joined'

class Role(str, enum.Enum):
    DEVELOPER = "developer"
    MANAGER = "manager"
    RECRUITER = "recruiter"
    CLIENT = "client"
    ADMIN = "admin"
    HR_MANAGER = "hr_manager"
    TECH_LEAD = "tech_lead"

class QuestionType(enum.Enum):
    Coding = 'Coding'
    MCQ = 'MCQ'
    Subjective = 'Subjective'
    Design = 'Design'
    Behavioral = 'Behavioral'

class DifficultyLevel(enum.Enum):
    Easy = 'Easy'
    Medium = 'Medium'
    Hard = 'Hard'

class ActivityType(enum.Enum):
    Application_Submitted = 'Application_Submitted'
    Resume_Screened = 'Resume_Screened'
    Interview_Scheduled = 'Interview_Scheduled'
    Interview_Completed = 'Interview_Completed'
    Offer_Extended = 'Offer_Extended'
    Offer_Accepted = 'Offer_Accepted'
    Offer_Declined = 'Offer_Declined'
    Onboarding_Started = 'Onboarding_Started'

class Department(str, enum.Enum):
    HR = "HR"
    TECHNICAL = "TECHNICAL"
    RECRUITMENT = "RECRUITMENT"
    CLIENT = "CLIENT"
    ADMIN = "ADMIN"

# Model definitions
class Organization(Base):
    __tablename__ = 'organization'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    department = Column(Enum(Department), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @staticmethod
    def create(user_name: str, email: str, password: str, department: Department):
        return Organization(
            user_name=user_name,
            email=email,
            password=password,
            password_hash=hash_password(password),
            department=department
        )

class HRDB(Base):
    __tablename__ = 'hr_db'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role_id = Column(Integer)
    credentials = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Role(Base):
    __tablename__ = 'roles'
    role_id = Column(Integer, primary_key=True)
    role_name = Column(String(255), unique=True, nullable=False)
    credentials = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    users = relationship('User', back_populates='role')

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.role_id'))
    credentials = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    role = relationship('Role', back_populates='users')
    subscriptions = relationship('Subscription', back_populates='user')

class Subscription(Base):
    __tablename__ = 'subscriptions'
    subscription_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    plan_name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    credentials = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    user = relationship('User', back_populates='subscriptions')
    
    __table_args__ = (
        CheckConstraint('end_date >= start_date', name='check_subscription_dates'),
    )

class Job(Base):
    __tablename__ = 'jobs'
    job_id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    threshold_score = Column(Float, nullable=False)
    credentials = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    candidates = relationship('Candidate', back_populates='job')
    questions = relationship('Question', back_populates='job')

class Candidate(Base):
    __tablename__ = 'candidates'
    candidate_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    resume_url = Column(String(255))
    job_id = Column(Integer, ForeignKey('jobs.job_id'))
    joining_score = Column(Float)
    status = Column(Enum(CandidateStatus), default=CandidateStatus.Applied)
    credentials = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    job = relationship('Job', back_populates='candidates')
    evaluations = relationship('Evaluation', back_populates='candidate')
    activities = relationship('Activity', back_populates='candidate')

class Evaluation(Base):
    __tablename__ = 'evaluations'
    evaluation_id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidates.candidate_id', ondelete='CASCADE'))
    job_id = Column(Integer, ForeignKey('jobs.job_id', ondelete='CASCADE'))
    score = Column(Float, nullable=False)
    feedback = Column(Text)
    credentials = Column(JSON, nullable=False)
    completed_at = Column(DateTime, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    candidate = relationship('Candidate', back_populates='evaluations')
    job = relationship('Job')

class Dashboard(Base):
    __tablename__ = 'dashboards'
    dashboard_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    title = Column(String(255), nullable=False)
    filters = Column(JSON, server_default='{}')
    credentials = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    user = relationship('User')

class Question(Base):
    __tablename__ = 'questions'
    question_id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.job_id', ondelete='CASCADE'))
    type = Column(Enum(QuestionType), nullable=False)
    difficulty = Column(Enum(DifficultyLevel), nullable=False)
    content = Column(Text, nullable=False)
    answer = Column(Text)
    credentials = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    job = relationship('Job', back_populates='questions')

class Activity(Base):
    __tablename__ = 'activities'
    
    activity_id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidates.candidate_id', ondelete='CASCADE'))
    activity_type = Column(SQLAlchemyEnum(ActivityType), nullable=False)  # Use SQLAlchemyEnum here
    timestamp = Column(DateTime, server_default=func.now())
    notes = Column(Text)
    credentials = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationship with Candidate
    candidate = relationship('Candidate', back_populates='activities')
class Notification(Base):
    __tablename__ = 'notifications'
    notification_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    message = Column(Text, nullable=False)
    read_status = Column(Boolean, default=False)
    credentials = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    user = relationship('User')

class Admin(Base):
    __tablename__ = 'admin'
    
    admin_id = Column(Integer, primary_key=True)
    username = Column(String(255),nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    mobile = Column(String(20), nullable=False)
    otp = Column(String(6), nullable=True)
    otp_created_at = Column(DateTime, nullable=True, server_default=func.now())
    department = Column(String(50), default='ADMIN')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


    @staticmethod
    def create(username: str, email: str, password: str, mobile: str):
        return Admin(
            username=username,
            email=email,
            password_hash=hash_password(password),
            mobile=mobile,
            department='ADMIN',
            is_active=True
        )

    def store_otp(self, otp: str):
        self.otp = otp
        self.otp_created_at = datetime.utcnow()


    def verify_otp(self, submitted_otp: str) -> bool:
        if not self.otp or not self.otp_created_at:
            return False
        # Check if OTP is not expired (e.g., within 5 minutes)
        is_valid_time = (datetime.now() - self.otp_created_at).total_seconds() < 300
        return self.otp == submitted_otp and is_valid_time

# Place Base.metadata.create_all here, after ALL models are defined
Base.metadata.create_all(bind=engine)

# Table mapping for data import
TABLE_MAPPING = {
    "HRDB": HRDB,
    "Roles": Role,
    "Users": User,
    "Subscriptions": Subscription,
    "Jobs": Job,
    "Candidates": Candidate,
    "Evaluations": Evaluation,
    "Dashboards": Dashboard,
    "Questions": Question,
    "Activities": Activity,
    "Notifications": Notification,
    "Organization": Organization,
    "Admin": Admin
}

def insert_initial_admin():
    db = SessionLocal()
    try:
        admin = Admin.create(
            username="admin",
            email="admin@fasthire.com",
            password="admin123",
            mobile="1234567890"
        )
        db.add(admin)
        db.commit()
        print("Initial admin created successfully")
    except Exception as e:
        db.rollback()
        print(f"Error creating admin: {e}")
    finally:
        db.close()

def init_db():
    """Initialize database with proper error handling"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        return False

def verify_admin_table():
    db = SessionLocal()
    try:
        admin = db.query(Admin).first()
        print("Admin table exists:", admin is not None)
    finally:
        db.close()

def process_json_fields(data):
    """Process JSON fields properly"""
    if isinstance(data, dict):
        return data
    try:
        return json.loads(data) if data else {}
    except:
        return {'data': str(data)}

def insert_data():
    """Insert data with comprehensive error handling and validation"""
    file_path = r"backend/final_fixed_subscriptions.xlsx"
    logger.info(f"Starting data insertion from: {file_path}")
    
    session = SessionLocal()
    insertion_stats = {}

    try:
        df = pd.ExcelFile(file_path)
        
        ordered_tables = [
            "HRDB", "Roles", "Users", "Jobs", "Candidates", 
            "Subscriptions", "Evaluations", "Questions", 
            "Activities", "Dashboards", "Notifications"
        ]
        
        for table_name in ordered_tables:
            if table_name not in df.sheet_names:
                logger.warning(f"Sheet {table_name} not found in Excel file")
                continue
                
            data = pd.read_excel(df, table_name)
            data.columns = [col.lower() for col in data.columns]
            records_inserted = 0
            
            for _, row in data.iterrows():
                try:
                    clean_data = {k: v for k, v in row.to_dict().items() if pd.notna(v)}
                    
                    # Handle JSON fields
                    if 'credentials' in clean_data:
                        clean_data['credentials'] = process_json_fields(clean_data['credentials'])
                    if 'filters' in clean_data:
                        clean_data['filters'] = process_json_fields(clean_data['filters'])
                    
                    # Handle datetime fields
                    for key, value in clean_data.items():
                        if isinstance(value, pd.Timestamp):
                            clean_data[key] = value.to_pydatetime()
                    
                    record = TABLE_MAPPING[table_name](**clean_data)
                    session.add(record)
                    session.commit()
                    records_inserted += 1
                    
                except Exception as e:
                    session.rollback()
                    logger.error(f"Error inserting record in {table_name}: {str(e)}")
                    continue
            
            insertion_stats[table_name] = records_inserted
            logger.info(f"Inserted {records_inserted} records into {table_name}")
            
        return insertion_stats
        
    except Exception as e:
        session.rollback()
        logger.error(f"Fatal error during data insertion: {str(e)}")
        return None
    finally:
        session.close()

def verify_data():
    """Verify data insertion with detailed reporting"""
    session = SessionLocal()
    verification_results = {}
    
    try:
        for table_name, model in TABLE_MAPPING.items():
            count = session.query(model).count()
            sample = session.query(model).first() if count > 0 else None
            
            verification_results[table_name] = {
                'count': count,
                'status': 'Success' if count > 0 else 'Empty',
                'sample': sample
            }
            
            logger.info(f"{table_name}: {count} records found")
            
        return verification_results
        
    except Exception as e:
        logger.error(f"Verification error: {str(e)}")
        return None
    finally:
        session.close()

def generate_report(insertion_stats, verification_results):
    """Generate comprehensive data insertion report"""
    report = {
        'timestamp': datetime.now().isoformat(),
        'summary': {},
        'details': {}
    }
    
    for table_name in TABLE_MAPPING.keys():
        inserted = insertion_stats.get(table_name, 0)
        verified = verification_results.get(table_name, {}).get('count', 0)
        
        report['summary'][table_name] = {
            'inserted': inserted,
            'verified': verified,
            'success': inserted == verified and inserted > 0
        }
        
    return report

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

@router.get("/status")
def get_db_status():
    return {"status": "Database is running"}

if __name__ == "__main__":
    logger.info("Starting database operations")
    
    create_fasthiredb()
    
    if init_db():
        insertion_stats = insert_data()
        if insertion_stats:
            insert_initial_admin()
            verification_results = verify_data()
            report = generate_report(insertion_stats, verification_results)
            logger.info("Operation completed successfully")
            logger.info(f"Final Report: {json.dumps(report['summary'], indent=2)}")
        else:
            logger.error("Data insertion failed, skipping verification and report generation")
