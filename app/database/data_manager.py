from typing import Dict, Optional, Any
from datetime import datetime
from .mongo_connection import insert_data, find_one

class DataManager:
    async def store_resume_insights(resume_id: int, parsed_data: Dict[str, Any]):
        resume_insights = {
            "resume_id": resume_id,
            "parsed_text": parsed_data.get("parsed_text", ""),
            "keywords_extracted": parsed_data.get("keywords", []),
            "skills_identified": parsed_data.get("skills", []),
            "experience_analysis": parsed_data.get("experience", {}),
            "education_analysis": parsed_data.get("education", {}),
            "insights": parsed_data.get("insights", {}),
            "generated_at": datetime.utcnow(),
        }
        return insert_data("resume_insights", resume_insights)

    async def store_candidate_evaluation(evaluation_id: int, candidate_id: int, evaluation_data: Dict[str, Any]):
        evaluation = {
            "evaluation_id": evaluation_id,
            "candidate_id": candidate_id,
            "ai_feedback": evaluation_data.get("feedback", {}),
            "skill_assessment": evaluation_data.get("skills", {}),
            "evaluation_summary": evaluation_data.get("summary", ""),
            "generated_at": datetime.utcnow(),
        }
        return insert_data("candidate_evaluations", evaluation)

    async def store_interview_transcription(interview_id: int, transcription_data: Dict[str, Any]):
        transcription = {
            "interview_id": interview_id,
            "transcription": {
                "full_text": transcription_data.get("text", ""),
                "segments": transcription_data.get("segments", []),
                "duration": transcription_data.get("duration", 0),
                "speaker_segments": transcription_data.get("speakers", []),
            },
            "analysis": transcription_data.get("analysis", {}),
            "keywords_extracted": transcription_data.get("keywords", []),
            "created_at": datetime.utcnow(),
        }
        return insert_data("interview_transcriptions", transcription)

    async def store_ai_questions(job_id: int, questions_data: Dict[str, Any]):
        questions = {
            "job_id": job_id,
            "questions": questions_data.get("questions", []),
            "question_categories": questions_data.get("categories", {}),
            "difficulty_distribution": questions_data.get("difficulty", {}),
            "generated_at": datetime.utcnow(),
            "last_updated": datetime.utcnow(),
        }
        return insert_data("ai_generated_questions", questions)

    async def get_resume_insights(resume_id: int) -> Optional[Dict]:
        return find_one("resume_insights", {"resume_id": resume_id})

    async def get_candidate_evaluation(evaluation_id: int) -> Optional[Dict]:
        return find_one("candidate_evaluations", {"evaluation_id": evaluation_id})

    async def get_interview_transcription(interview_id: int) -> Optional[Dict]:
        return find_one("interview_transcriptions", {"interview_id": interview_id})

    async def get_ai_questions(job_id: int) -> Optional[Dict]:
        return find_one("ai_generated_questions", {"job_id": job_id})
