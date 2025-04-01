# routers/recruiters.py
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app1.models.skill_model import RecruiterCreate, RecruiterResponse
from app1.database.session import get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import text
from uuid import UUID

router = APIRouter(
    prefix="/api/recruiters",
    tags=["recruiters"]
)

@router.get("", response_model=List[RecruiterResponse])
async def get_recruiters(db: Session = Depends(get_db)):
    # Using SQLAlchemy's text() for raw SQL
    result = db.execute(text("SELECT * FROM recruiters ORDER BY name"))
    recruiters = result.mappings().all()
    # Convert to list of dictionaries
    recruiter_list = []
    for recruiter in recruiters:
        recruiter_dict = dict(recruiter)
        # Convert UUID to string if needed for serialization
        if isinstance(recruiter_dict.get("id"), UUID):
            recruiter_dict["id"] = recruiter_dict["id"]
        recruiter_list.append(recruiter_dict)            
    return recruiter_list

@router.get("/{recruiter_id}", response_model=RecruiterResponse)
async def get_recruiter(recruiter_id: str, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM recruiters WHERE id = :id"), {"id": recruiter_id})
    recruiter = result.mappings().first()
    if not recruiter:
        raise HTTPException(status_code=404, detail="Recruiter not found")
    return dict(recruiter)

@router.post("", response_model=RecruiterResponse)
async def create_recruiter(recruiter: RecruiterCreate, db: Session = Depends(get_db)):
    # Adjust the query to match the actual table structure
    query = text("""
        INSERT INTO recruiters (name, phone_number, skills, role, experience) 
        VALUES (:name, :phone_number, :skills, :role, :experience) 
        RETURNING *
    """)
    result = db.execute(
        query,
        {
            "name": recruiter.name, 
            "phone_number": recruiter.phone_number,
            "skills": recruiter.skills,
            "role": recruiter.role,
            "experience": recruiter.experience
        }
    )
    new_recruiter = result.mappings().first()
    db.commit()
    
    return dict(new_recruiter)

@router.put("/{recruiter_id}", response_model=RecruiterResponse)
async def update_recruiter(recruiter_id: str, recruiter: RecruiterCreate, db: Session = Depends(get_db)):
    # Check if recruiter exists
    check_query = text("SELECT id FROM recruiters WHERE id = :id")
    result = db.execute(check_query, {"id": recruiter_id})
    if not result.first():
        raise HTTPException(status_code=404, detail="Recruiter not found")
    
    # Update recruiter with the correct fields
    update_query = text("""
        UPDATE recruiters 
        SET name = :name, phone_number = :phone_number, skills = :skills, role = :role, experience = :experience
        WHERE id = :id
        RETURNING *
    """)
    
    result = db.execute(
        update_query,
        {
            "name": recruiter.name, 
            "phone_number": recruiter.phone_number,
            "skills": recruiter.skills,
            "role": recruiter.role,
            "experience": recruiter.experience,
            "id": recruiter_id
        }
    )
    
    updated_recruiter = result.mappings().first()
    db.commit()
    
    return dict(updated_recruiter)

@router.delete("/{recruiter_id}")
async def delete_recruiter(recruiter_id: str, db: Session = Depends(get_db)):
    # Check if recruiter exists
    check_query = text("SELECT id FROM recruiters WHERE id = :id")
    result = db.execute(check_query, {"id": recruiter_id})
    if not result.first():
        raise HTTPException(status_code=404, detail="Recruiter not found")
    
    # Delete recruiter
    delete_query = text("DELETE FROM recruiters WHERE id = :id")
    db.execute(delete_query, {"id": recruiter_id})
    db.commit()
    
    return {"message": "Recruiter deleted successfully"}