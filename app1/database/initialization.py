import psycopg2
import logging
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_db_connection(
    host='localhost', 
    database='fasthire99', 
    user='postgres', 
    password='Temp1234', 
    port=5432
):
    """
    Establish and return a database connection
    """
    try:
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        conn.autocommit = True
        logger.info("Database connection established successfully")
        return conn
    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error connecting to database: {error}")
        raise

def close_db_connection(conn):
    """
    Close the database connection
    """
    try:
        if conn:
            conn.close()
            logger.info("Database connection closed")
    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error closing database connection: {error}")

def init_db(
    host='localhost', 
    database='fasthire99', 
    user='postgres', 
    password='Temp1234', 
    port=5432
):
    """
    Initialize database tables with SQLAlchemy model definitions
    """
    conn = None
    try:
        # Establish connection
        conn = get_db_connection(host, database, user, password, port)
        
        # Create cursor
        cursor = conn.cursor()
        
        # Create job_descriptions table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_descriptions (
            job_id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            title VARCHAR NOT NULL,
            description VARCHAR NOT NULL,
            threshold_score FLOAT NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Create job_required_skills table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_required_skills (
            id SERIAL PRIMARY KEY,
            job_id INTEGER,
            FOREIGN KEY (job_id) REFERENCES job_descriptions(job_id) ON DELETE CASCADE
        )
        """)
        
        # Create threshold_scores table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS threshold_scores (
            threshold_id SERIAL PRIMARY KEY,
            job_id INTEGER,
            selection_score FLOAT NOT NULL,
            rejection_score FLOAT NOT NULL,
            threshold_value FLOAT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (job_id) REFERENCES job_descriptions(job_id) ON DELETE CASCADE
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_analyses (
            id SERIAL PRIMARY KEY,
            roles JSONB,
            skills_data JSONB,
            content TEXT,
            selection_threshold FLOAT,
            rejection_threshold FLOAT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
        """)

        logger.info("Database tables created successfully")
        return conn
    
    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error initializing database: {error}")
        if conn:
            close_db_connection(conn)
        raise
    finally:
        # Ensure cursor is closed
        if 'cursor' in locals():
            cursor.close()

# Example database connection string for SQLAlchemy
def get_sqlalchemy_engine(
    host='localhost', 
    database='fasthire99', 
    user='postgres', 
    password='Temp1234', 
    port=5432
):
    """
    Create SQLAlchemy engine for ORM operations
    """
    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    try:
        engine = create_engine(connection_string)
        logger.info("SQLAlchemy engine created successfully")
        return engine
    except Exception as error:
        logger.error(f"Error creating SQLAlchemy engine: {error}")
        raise

# Example usage
if __name__ == "__main__":
    try:
        # Initialize PostgreSQL tables
        connection = init_db(
            host='localhost',
            database='fasthire99',
            user='postgres',
            password='Temp1234',
            port=5432
        )
        
        # Create SQLAlchemy engine
        engine = get_sqlalchemy_engine(
            host='localhost',
            database='fasthire99',
            user='postgres',
            password='Temp1234',
            port=5432
        )
        
        logger.info("Database initialization complete")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
    finally:
        if 'connection' in locals():
            close_db_connection(connection)