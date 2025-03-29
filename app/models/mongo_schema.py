from pymongo import MongoClient, ASCENDING
from datetime import datetime
from typing import Dict, List

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["fasthire"]


def create_resume_insights_collection():
    resume_insights = {
        "resume_id": int,
        "candidate_id": int,
        "job_id": int,
        "parsed_text": str,
        "keywords_extracted": List[str],
        "skills_identified": List[str],
        "experience_analysis": {
            "years_experience": float,
            "relevant_experience": str,
            "key_achievements": List[str],
        },
        "education_analysis": {
            "degrees": List[str],
            "institutions": List[str],
            "graduation_years": List[int],
        },
        "insights": {
            "strengths": str,
            "weaknesses": str,
            "recommendations": str,
            "skill_match_score": float,
        },
        "generated_at": datetime,
    }
    db.resume_insights.create_index([("resume_id", ASCENDING)])
    return resume_insights


def create_candidate_evaluation_collection():
    candidate_eval = {
        "evaluation_id": int,
        "candidate_id": int,
        "job_id": int,
        "ai_feedback": {
            "overall_score": float,
            "technical_score": float,
            "communication_score": float,
            "experience_score": float,
            "strengths": List[str],
            "weaknesses": List[str],
            "recommendations": List[str],
        },
        "skill_assessment": {
            "required_skills": List[str],
            "matched_skills": List[str],
            "missing_skills": List[str],
            "skill_scores": Dict[str, float],
        },
        "evaluation_summary": str,
        "generated_at": datetime,
    }
    db.candidate_evaluations.create_index([("candidate_id", ASCENDING)])
    db.candidate_evaluations.create_index([("evaluation_id", ASCENDING)])
    return candidate_eval

def create_interview_transcription_collection():
    interview_transcription = {
        "interview_id": int,
        "candidate_id": int,
        "job_id": int,
        "transcription": {
            "full_text": str,
            "segments": List[Dict],
            "duration": float,
            "speaker_segments": List[Dict],
        },
        "analysis": {
            "sentiment_analysis": {
                "overall_sentiment": float,
                "sentiment_breakdown": Dict[str, float],
                "key_moments": List[Dict],
            },
            "technical_analysis": {
                "technical_accuracy": float,
                "concept_understanding": float,
                "problem_solving": float,
            },
            "communication_analysis": {
                "clarity": float,
                "confidence": float,
                "articulation": float,
            },
        },
        "keywords_extracted": List[str],
        "created_at": datetime,
    }
    db.interview_transcriptions.create_index([("interview_id", ASCENDING)])
    return interview_transcription

def create_ai_questions_collection():
    ai_questions = {
        "job_id": int,
        "questions": List[Dict],
        "question_categories": {
            "technical": List[Dict],
            "behavioral": List[Dict],
            "experience": List[Dict],
            "role_specific": List[Dict],
        },
        "difficulty_distribution": {
            "easy": List[int],
            "medium": List[int],
            "hard": List[int],
        },
        "generated_at": datetime,
        "last_updated": datetime,
    }
    db.ai_generated_questions.create_index([("job_id", ASCENDING)])
    return ai_questions

def initialize_mongodb_collections():
    collections = {
        "resume_insights": create_resume_insights_collection(),
        "candidate_evaluations": create_candidate_evaluation_collection(),
        "interview_transcriptions": create_interview_transcription_collection(),
        "ai_generated_questions": create_ai_questions_collection(),
    }

    print("\nInitializing MongoDB Collections...")
    for name, schema in collections.items():
        print(f"✓ Initialized {name} collection")

    return collections


# Create all collections when module is imported
MONGODB_SCHEMAS = initialize_mongodb_collections()
