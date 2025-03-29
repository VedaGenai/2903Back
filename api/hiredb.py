import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .fasthire_db import (
    User, 
    Role,
    get_db, 
    CandidateStatus, 
    Organization,
    Admin, 
    Department,
    hash_password
)  
import random
from enum import Enum
from pydantic import BaseModel, EmailStr, ConfigDict, validator
from datetime import datetime
from typing import Optional, List, Dict, Literal
import secrets
from passlib.context import CryptContext
from datetime import timedelta
from jose import jwt

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Setup router
router = APIRouter()

# Authentication configuration
SECRET_KEY = "your-secret-key"  # In production, use a secure secret key
ALGORITHM = "HS256"

# Authentication helper functions
def verify_password(plain_password, hashed_password):
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    """Create a JWT access token"""
    to_encode = data.copy()
    expires = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expires})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# -------------------- Pydantic Models --------------------

# User Models
class UserResponse(BaseModel):
    """Schema for user response data"""
    user_id: int
    username: str
    name: str
    email: str
    role_id: int
    credentials: dict
    
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    """Schema for creating a new user"""
    username: str
    name: str
    email: str
    password: str
    role_id: int
    credentials: dict = {"active": True}

# Role Models
class RoleBase(BaseModel):
    """Base schema for role data"""
    role_name: str
    credentials: dict

class RoleCreate(RoleBase):
    """Schema for creating a new role"""
    pass

class RoleResponse(RoleBase):
    """Schema for role response data"""
    role_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Department Enum
class DepartmentEnum(str, Enum):
    """Enum representing different departments"""
    HR = "HR"
    CLIENT = "CLIENT"
    RECRUITMENT = "RECRUITMENT"
    TECHNICAL = "TECHNICAL"

# Organization Models
class OrganizationCreate(BaseModel):
    """Schema for creating a new organization"""
    user_name: str
    email: str
    password: str 
    department: str

class OrganizationResponse(BaseModel):
    """Schema for organization response data"""
    id: int
    user_name: str
    email: str
    department: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Admin Models
class AdminCreate(BaseModel):
    """Schema for creating a new admin"""
    username: str
    email: EmailStr
    password: str
    mobile: str
    
class AdminResponse(BaseModel):
    """Schema for admin response data"""
    admin_id: int
    username: str
    email: str
    mobile: str
    department: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Authentication Models
class OTPRequest(BaseModel):
    """Schema for OTP request"""
    email: EmailStr
    mobile: str

class LoginRequest(BaseModel):
    """Schema for login request"""
    email: str
    password: str

# -------------------- API Routes --------------------

# User Routes
@router.get("/users", response_model=List[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    """Get all users"""
    return db.query(User).all()

@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    # Create new user
    new_user = User(
        username=user.username,
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password),
        role_id=user.role_id,
        credentials=user.credentials
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Role Routes
@router.get("/roles", response_model=List[RoleResponse])
def get_roles(db: Session = Depends(get_db)):
    """Get all roles"""
    return db.query(Role).all()

@router.post("/roles", response_model=RoleResponse)
async def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    """Create a new role"""
    # Check if role already exists
    existing_role = db.query(Role).filter(Role.role_name == role.role_name).first()
    if existing_role:
        raise HTTPException(status_code=400, detail=f"Role with name '{role.role_name}' already exists")
    
    # Create new role
    new_role = Role(role_name=role.role_name, credentials=role.credentials)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

@router.get("/roles/{role_id}", response_model=RoleResponse)
async def get_role(role_id: int, db: Session = Depends(get_db)):
    """Get a role by ID"""
    role = db.query(Role).filter(Role.role_id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.put("/roles/{role_id}", response_model=RoleResponse)
async def update_role(role_id: int, role_update: RoleBase, db: Session = Depends(get_db)):
    """Update a role"""
    # Check if role exists
    db_role = db.query(Role).filter(Role.role_id == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    # Check if updated role name already exists
    if role_update.role_name:
        existing_role = db.query(Role).filter(
            Role.role_name == role_update.role_name,
            Role.role_id != role_id
        ).first()
        if existing_role:
            raise HTTPException(status_code=400, detail=f"Role name '{role_update.role_name}' already exists")
    
    # Update role attributes
    for key, value in role_update.model_dump().items():  # Changed from dict() to model_dump()
        setattr(db_role, key, value)
    
    db.commit()
    db.refresh(db_role)
    return db_role

# Organization Routes
@router.get("/organizations", response_model=List[OrganizationResponse])
async def get_organizations(db: Session = Depends(get_db)):
    """Get all organizations"""
    organizations = db.query(Organization).all()
    return organizations

@router.post("/organizations", response_model=OrganizationResponse)
async def create_organization(org: OrganizationCreate, db: Session = Depends(get_db)):
    """Create a new organization"""
    try:
        # Check if email already exists
        existing_org = db.query(Organization).filter(
            Organization.email == org.email
        ).first()
        
        if existing_org:
            raise HTTPException(status_code=400, detail="Email already exists")

        # Convert string department to enum
        department_enum = Department[org.department]  # Fixed conversion from str to Enum

        # Create new organization
        new_org = Organization.create(
            user_name=org.user_name,
            email=org.email,
            password=org.password,
            department=department_enum
        )
        
        db.add(new_org)
        db.commit()
        db.refresh(new_org)
        return new_org

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/organizations/{org_id}")
async def delete_organization(org_id: int, db: Session = Depends(get_db)):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    db.delete(org)
    db.commit()
    return {"message": "Organization deleted successfully"}

@router.put("/organizations/{org_id}", response_model=OrganizationResponse)
async def update_organization(
    org_id: int, 
    org_update: OrganizationCreate, 
    db: Session = Depends(get_db)
):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    org.user_name = org_update.user_name
    org.email = org_update.email
    org.department = org_update.department
    if org_update.password:
        org.password_hash = hash_password(org_update.password)
    
    db.commit()
    db.refresh(org)
    return org


# Admin Routes
@router.post("/admin", response_model=AdminResponse)
async def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    # Check only for existing email
    existing_email = db.query(Admin).filter(Admin.email == admin.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_admin = Admin.create(
        username=admin.username,
        email=admin.email,
        password=admin.password,
        mobile=admin.mobile
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

@router.post("/send-otp")
async def send_otp(request: OTPRequest, db: Session = Depends(get_db)):
    """Send OTP to user"""
    # Generate 6-digit OTP
    otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    
    # Check if admin already exists
    admin = db.query(Admin).filter(
        (Admin.email == request.email) & (Admin.mobile == request.mobile)
    ).first()
    
    # Create temporary admin if not exists
    if not admin:
        temp_password = "temp" + otp
        admin = Admin.create(
            username=request.email.split('@')[0],
            email=request.email,
            password=temp_password,
            mobile=request.mobile
        )
        db.add(admin)
    
    # Store OTP for verification
    admin.store_otp(otp)
    db.commit()
    
    # For development/testing
    print(f"OTP for testing: {otp}")
    
    return {"message": "OTP sent successfully"}

# Authentication route
@router.post("/login")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate a user"""
    # First check Admin table
    admin = db.query(Admin).filter(Admin.email == login_data.email).first()
    if admin:
        if verify_password(login_data.password, admin.password_hash):
            # Return admin login response
            return {
                "message": "Login successful",
                "department": "ADMIN",
                "redirect_to": "/Admin"
            }
        raise HTTPException(status_code=401, detail="Invalid password")
        
     
    # Then check Organization table
    org_user = db.query(Organization).filter(Organization.email == login_data.email).first()
    if org_user:
        if verify_password(login_data.password, org_user.password_hash):
            # Return organization login response
            return {
                "message": "Login successful",
                "department": org_user.department.value,
                "redirect_to": get_department_route(org_user.department)
            }
        raise HTTPException(status_code=401, detail="Invalid password")
    # Return error if authentication fails
    raise HTTPException(status_code=401, detail="Email not found. Please register first.")

def get_department_route(department: Department):
    """Get redirect route based on department"""
    routes = {
        Department.HR: "/hiring",
        Department.TECHNICAL: "/Technical", 
        Department.RECRUITMENT: "/recruiter/rec_ui",
        Department.CLIENT: "/client"
    }
    return routes.get(department, "/dashboard")