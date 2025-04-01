from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.routes.skills_evaluation import analyze_job_description_router
from app.routes.recruiters import router as router1
from app.routes.upload import router
from app1.database.initialization import init_db
app = FastAPI()

# Configure CORS with more permissive settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,  # Must be False when allow_origins=["*"]
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"]  # Expose all headers
)

# Include the routers
app.include_router(analyze_job_description_router, prefix="/api")
app.include_router(router, prefix="/api")
app.include_router(router1)

@app.on_event("startup")
async def startup_event():
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("uploads/resumes", exist_ok=True)
    os.makedirs("uploads/jobs", exist_ok=True)
    try:
        init_db()
    except Exception as e:
        print(f"Database initialization failed: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)