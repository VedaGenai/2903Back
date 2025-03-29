from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
import shutil
from datetime import datetime

router = APIRouter()

UPLOAD_DIRECTORY = "uploads"  # Directory to store uploaded files

# Create the upload directory if it doesn't exist
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@router.post("/upload_file/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Generate a unique file ID
        file_id = str(uuid.uuid4())
        
        # Create a filename that includes the original filename and the UUID
        filename = f"{file_id}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIRECTORY, filename)
        
        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Store file metadata in database or file system
        file_metadata = {
            "file_id": file_id,
            "original_filename": file.filename,
            "saved_path": file_path,
            "upload_date": datetime.now().isoformat(),
            "file_type": file.content_type
        }
        
        # Here you would typically save this metadata to a database
        # For example: db.file_metadata.insert_one(file_metadata)
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "File uploaded successfully",
                "file_id": file_id,
                "filename": file.filename
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during file upload: {str(e)}"
        )