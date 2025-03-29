# # __all__ = ["app", "core", "database", "models", "routes", "services", "tempates", "utils", "uploads"]

# # from fastapi import FastAPI
# # from .routes import router
# # from fastapi.middleware.cors import CORSMiddleware
# # from app.services.llm_service import LLMService
# # from app.routes.resume_evaluation import resume_evaluation_router
# # from app.routes.skills_evaluation import analyze_job_description_router, create_dashboards_router

# # app = FastAPI(title="FastHire99 API", version="1.0.0")

# # # CORS Configuration
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],  # Allow all origins for testing
# #     allow_credentials=False,  # Must be False when using allow_origins=["*"]
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # Router configurations
# # app.include_router(resume_evaluation_router, tags=["Resume"])
# # app.include_router(analyze_job_description_router, prefix="/api", tags=["Job Analysis"])
# # app.include_router(create_dashboards_router, prefix="/api", tags=["Dashboards"])
# __all__ = ["app", "core", "database", "models", "routes", "services", "tempates", "utils", "uploads"]

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.services.llm_service import LLMService
# from app.routes.resume_evaluation import resume_evaluation_router
# from app.routes.skills_evaluation import analyze_job_description_router, create_dashboards_router

# app = FastAPI(title="FastHire99 API", version="1.0.0")

# # CORS Configuration
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all origins for testing
#     allow_credentials=False,  # Must be False when using allow_origins=["*"]
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Router configurations
# app.include_router(resume_evaluation_router, tags=["Resume"])
# app.include_router(analyze_job_description_router, prefix="/api", tags=["Job Analysis"])
# app.include_router(create_dashboards_router, prefix="/api", tags=["Dashboards"])
__all__ = ["app", "core", "database", "models", "routes", "services", "tempates", "utils", "uploads"]

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.llm_service import LLMService
from app.routes.resume_evaluation import resume_evaluation_router
from app.routes.skills_evaluation import (
    analyze_job_description_router, 
)

app = FastAPI(title="FastHire99 API", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router configurations
app.include_router(resume_evaluation_router, tags=["Resume"])
app.include_router(analyze_job_description_router, prefix="/api", tags=["Job Analysis"])