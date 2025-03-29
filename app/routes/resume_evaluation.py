from fastapi import APIRouter, File, UploadFile, Form
from ..core.prompt_engineering import PromptEngineering
from app.services.llm_service import LLMService
from app.utils.helpers import process_pdf, handle_role_selection
from fastapi.responses import JSONResponse
from ..core.Config import logger 
import logging
logger = logging.getLogger(__name__)


resume_evaluation_router = APIRouter(tags=["Resume Evaluation"])

@resume_evaluation_router.post("/upload-resume")
async def upload_resume_endpoint(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = (
            process_pdf(content)
            if file.filename.endswith('.pdf')
            else process_pdf(content)  # Changed to process_pdf for both cases
        )
        
        # Remove the call to extract_resume_sections as it's not defined
        
        return JSONResponse(
            content={
                "status": "success",
                "text": text,
                "file_type": "pdf" if file.filename.endswith('.pdf') else "word"
            },
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "error": str(e)},
            status_code=500
        )

@resume_evaluation_router.post("/generate-dashboards")
async def generate_dashboards_endpoint(
    file: UploadFile = File(...),
    num_sections: int = Form(default=9)
):
    try:
        content = await file.read()
        text = (
            process_pdf(content)
            if file.filename.endswith('.pdf')
            else process_pdf(content)
        )
        

        sections = handle_role_selection(text)
        dashboards = PromptEngineering.generate_dashboards_prompt(text, sections, num_sections)
        
        return JSONResponse(
            content={"status": "success", "dashboards": dashboards},
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "error": str(e)},
            status_code=500
        )

@resume_evaluation_router.post("/generate-custom-dashboard")
async def generate_custom_dashboard_endpoint(
    file: UploadFile = File(...),
    prompt: str = Form(...)
):
    try:
        content = await file.read()
        text = (
            process_pdf(content)
            if file.filename.endswith('.pdf')
            else process_pdf(content)
        )
        
        sections = handle_role_selection(text)
        dashboard = PromptEngineering.generate_custom_dashboard_prompt(sections, prompt)
        
        return JSONResponse(
            content={"status": "success", "dashboard": dashboard},
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "error": str(e)},
            status_code=500
        )
@resume_evaluation_router.post("/generate-sample-prompts")
async def generate_sample_prompts_endpoint(
    file: UploadFile = File(None),
    num_prompts: int = Form(default=5)
):
    try:
        if not file:
            return JSONResponse(
                content={
                    "status": "success",
                    "prompts": [f"Sample Prompt {i}" for i in range(1, num_prompts + 1)]
                },
                status_code=200
            )

        content = await file.read()
        text = (
            process_pdf(content)
            if file.filename.endswith('.pdf')
            else process_pdf(content)
        )
        
        sections = handle_role_selection(text)
        
        sample_prompts = []
        for header in list(sections.keys())[:num_prompts]:
            prompt = f"Generate {header} Dashboard"
            sample_prompts.append(prompt)
        
        while len(sample_prompts) < num_prompts:
            sample_prompts.append(f"Additional Dashboard {len(sample_prompts) + 1}")
        
        return JSONResponse(
            content={
                "status": "success",
                "prompts": sample_prompts
            },
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "error": str(e)},
            status_code=500

        )

# Audio Processing Endpoints
@resume_evaluation_router.post("/start-recording")
async def start_recording():
    try:
        result = PromptEngineering.start_recording()
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@resume_evaluation_router.post("/stop-recording")
async def stop_recording():
    try:
        result = PromptEngineering.stop_recording()
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@resume_evaluation_router.post("/transcribe")
async def transcribe_audio(filename: str):
    try:
        result = PromptEngineering.transcribe_audio(filename)
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# QA Generation Endpoints
@resume_evaluation_router.post("/generate-qa")
async def generate_qa_endpoint(
    section_content: str = Form(...),
    num_questions: int = Form(default=5)
):
    try:
        result = PromptEngineering.generate_qa_prompt(section_content, num_questions)
        
        if result["status"] == "success":
            return JSONResponse(content=result, status_code=200)
        else:
            return JSONResponse(content=result, status_code=500)
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return JSONResponse(
            content={"status": "error", "error": str(e)},
            status_code=500
        )
      
    
@resume_evaluation_router.post("/generate-follow-up")
async def generate_follow_up(
    question: str = Form(...),
    answer: str = Form(...)
):
    try:
        follow_up_prompt = PromptEngineering.generate_follow_up_prompt(question, answer)
        return JSONResponse(content={"prompt": follow_up_prompt}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
