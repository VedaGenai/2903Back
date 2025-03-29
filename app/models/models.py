# Assuming this is where your models are defined
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class JobDescription(Base):
    __tablename__ = 'job_descriptions'
    
    # Change this line if it's different - ensure the primary key is named 'job_id'
    job_id = Column(Integer, primary_key=True)
    # Other columns...

class Discussion(Base):
    __tablename__ = 'discussions'
    
    id = Column(Integer, primary_key=True)
    # Make sure this foreign key references the correct column
    job_id = Column(Integer, ForeignKey('job_descriptions.job_id'))
    # Other columns...
