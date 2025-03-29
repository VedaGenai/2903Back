from mongo_connection import insert_data, delete_many
from datetime import datetime, timedelta
import random

# Sample data for companies
companies = [
    {
        "_id": "comp_1",
        "name": "Tech Innovators Inc.",
        "industry": "Technology",
        "size": "500-1000",
        "location": "San Francisco, CA",
        "description": "Leading software development company",
        "website": "www.techinnovators.com",
        "founded_year": 2010,
    },
    {
        "_id": "comp_2",
        "name": "Global Finance Solutions",
        "industry": "Finance",
        "size": "1000+",
        "location": "New York, NY",
        "description": "International financial services provider",
        "website": "www.globalfinance.com",
        "founded_year": 2005,
    },
    {
        "_id": "comp_3",
        "name": "Healthcare Plus",
        "industry": "Healthcare",
        "size": "200-500",
        "location": "Boston, MA",
        "description": "Modern healthcare solutions provider",
        "website": "www.healthcareplus.com",
        "founded_year": 2015,
    },
]

# Sample skills data
skills = [
    {"_id": "skill_1", "name": "Python", "category": "Programming Language"},
    {"_id": "skill_2", "name": "JavaScript", "category": "Programming Language"},
    {"_id": "skill_3", "name": "React", "category": "Frontend Framework"},
    {"_id": "skill_4", "name": "Node.js", "category": "Backend Framework"},
    {"_id": "skill_5", "name": "MongoDB", "category": "Database"},
    {"_id": "skill_6", "name": "AWS", "category": "Cloud Platform"},
    {"_id": "skill_7", "name": "Docker", "category": "DevOps"},
    {"_id": "skill_8", "name": "Machine Learning", "category": "Data Science"},
]

# Sample job postings
job_postings = [
    {
        "_id": "job_1",
        "company_id": "comp_1",
        "title": "Senior Software Engineer",
        "description": "Looking for an experienced software engineer to lead our backend team",
        "required_skills": ["skill_1", "skill_4", "skill_5"],
        "experience_level": "Senior",
        "employment_type": "Full-time",
        "location": "San Francisco, CA",
        "salary_range": {"min": 120000, "max": 180000},
        "posted_date": datetime.now() - timedelta(days=5),
        "status": "Active",
    },
    {
        "_id": "job_2",
        "company_id": "comp_2",
        "title": "Frontend Developer",
        "description": "Seeking a creative frontend developer with React expertise",
        "required_skills": ["skill_2", "skill_3"],
        "experience_level": "Mid-level",
        "employment_type": "Full-time",
        "location": "New York, NY",
        "salary_range": {"min": 90000, "max": 130000},
        "posted_date": datetime.now() - timedelta(days=3),
        "status": "Active",
    },
    {
        "_id": "job_3",
        "company_id": "comp_3",
        "title": "DevOps Engineer",
        "description": "Looking for a DevOps engineer to improve our deployment pipeline",
        "required_skills": ["skill_6", "skill_7"],
        "experience_level": "Mid-level",
        "employment_type": "Full-time",
        "location": "Boston, MA",
        "salary_range": {"min": 100000, "max": 150000},
        "posted_date": datetime.now() - timedelta(days=7),
        "status": "Active",
    },
]

# Sample candidates data
candidates = [
    {
        "_id": "cand_1",
        "first_name": "John",
        "last_name": "Smith",
        "email": "john.smith@email.com",
        "phone": "+1-555-0123",
        "location": "San Francisco, CA",
        "skills": ["skill_1", "skill_2", "skill_4"],
        "experience": [
            {
                "title": "Software Engineer",
                "company": "Previous Tech Co",
                "duration": "2018-2023",
                "description": "Led backend development team",
            }
        ],
        "education": [
            {
                "degree": "BS Computer Science",
                "institution": "Stanford University",
                "year": 2018,
            }
        ],
        "preferred_job_type": "Full-time",
        "preferred_location": "San Francisco Bay Area",
        "expected_salary": 130000,
    },
    {
        "_id": "cand_2",
        "first_name": "Emily",
        "last_name": "Johnson",
        "email": "emily.j@email.com",
        "phone": "+1-555-0124",
        "location": "New York, NY",
        "skills": ["skill_2", "skill_3", "skill_6"],
        "experience": [
            {
                "title": "Frontend Developer",
                "company": "Web Solutions Inc",
                "duration": "2019-2023",
                "description": "Developed responsive web applications",
            }
        ],
        "education": [
            {"degree": "MS Web Development", "institution": "NYU", "year": 2019}
        ],
        "preferred_job_type": "Full-time",
        "preferred_location": "New York City",
        "expected_salary": 110000,
    },
]


def clear_existing_data():
    """Clear existing data from all collections"""
    collections = ["companies", "skills", "job_postings", "candidates"]
    for collection in collections:
        print(f"Clearing {collection} collection...")
        delete_many(collection, {})


def insert_sample_data():
    """Insert sample data into the database"""
    try:
        # Clear existing data first
        clear_existing_data()

        # Insert data into collections
        print("\nInserting sample data...")

        print("Inserting companies...")
        insert_data("companies", companies)

        print("Inserting skills...")
        insert_data("skills", skills)

        print("Inserting job postings...")
        insert_data("job_postings", job_postings)

        print("Inserting candidates...")
        insert_data("candidates", candidates)

        print("\n✅ Sample data inserted successfully!")

    except Exception as e:
        print(f"\n❌ Error inserting sample data: {str(e)}")
        raise


if __name__ == "__main__":
    insert_sample_data()
