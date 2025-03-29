from pymongo import MongoClient, ASCENDING
from datetime import datetime
from typing import Dict, List, Any, Optional

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
        "ai_generated_qa": List[Dict[str, Any]],

        "generated_at": datetime,
    }
    db.resume_insights.create_index([("resume_id", ASCENDING)])
    return resume_insights


def create_job_description_collection():
    """Create a structured schema for storing job descriptions"""
    job_description_schema = {
        "job_id": int,  # Reference to SQL job_id
        "title": str,
        "source_file": str,
        "upload_date": datetime,
        "status": str,  # Active, Archived, etc.
        
        # Structured sections from the JD
        "sections": {
            "career_level_summary": str,
            "critical_competencies": List[Dict[str, str]],  # [{"name": "Systems Thinking", "description": "..."}]
            "key_responsibilities": List[str],
            "person_specification": {
                "knowledge": List[str],
                "skills": List[str],
                "education": List[str],
                "experience": List[str],
                "physical_demands": List[str]
            }
        },
        
        # Job metadata
        "metadata": {
            "role": str,  # e.g., "Site Reliability Engineer"
            "industry_type": str,  # e.g., "IT Services & Consulting"
            "department": str,  # e.g., "Engineering - Software & QA"
            "employment_type": str,  # e.g., "Full Time, Permanent"
            "role_category": str,  # e.g., "DevOps"
            "education_level": {
                "undergraduate": str,  # e.g., "Any Graduate"
                "postgraduate": str  # e.g., "Any Postgraduate"
            }
        },
        
        # Extracted skills and keywords
        "key_skills": List[str],  # List of all key skills mentioned
        "technical_skills": List[str],  # Specifically technical skills
        "soft_skills": List[str],  # Soft/interpersonal skills
        
        # AI analysis results
        "ai_analysis": {
            "role_importance": Dict[str, float],  # Importance scores for different aspects
            "required_skills": List[Dict[str, Any]],  # [{"name": "Python", "importance": 80, "selection_score": 75, "rejection_score": 85}]
            "experience_requirements": {
                "min_years": float,
                "preferred_years": float,
                "domains": List[str]  # Specific domains where experience is needed
            },
            "education_requirements": {
                "min_degree": str,
                "preferred_degree": str,
                "fields": List[str]  # Fields of study
            },
            "culture_fit_indicators": List[str],  # Cultural aspects mentioned in JD
            "summary": str  # AI-generated summary of the position
        },
        
        # Timestamps
        "created_at": datetime,
        "updated_at": datetime,
        "analyzed_at": Optional[datetime]
    }
    
    # Create index on job_id for fast lookups
    db.job_descriptions.create_index([("job_id", ASCENDING)])
    db.job_descriptions.create_index([("title", "text"), ("sections.key_responsibilities", "text")])
    
    return job_description_schema

def create_jd_insights_collection():
    """Enhanced schema for storing JD insights and analysis"""
    jd_insights = {
        "job_id": int,  # Reference to SQL job_id
        "title": str,  # Job title
        "created_at": datetime,
        
        # Extracted text sections
        "parsed_sections": {
            "career_summary": str,
            "competencies": str,
            "responsibilities": str,
            "knowledge_requirements": str,
            "skill_requirements": str,
            "education_requirements": str,
            "experience_requirements": str,
            "physical_demands": str,
            "role_metadata": str  # Role, industry, department, etc.
        },
        
        # Extracted entities
        "extracted_entities": {
            "job_titles": List[str],
            "skills": List[str],
            "technologies": List[str],
            "certifications": List[str],
            "education_levels": List[str],
            "experience_levels": List[str],
            "locations": List[str],
            "companies": List[str],
            "industries": List[str]
        },
        
        # Skill analysis
        "skill_analysis": {
            "technical_skills": List[Dict[str, Any]],  # [{"name": "Python", "importance": 80, "selection_weight": 75, "rejection_weight": 85}]
            "soft_skills": List[Dict[str, Any]],
            "domain_knowledge": List[Dict[str, Any]],
            "certifications": List[Dict[str, Any]]
        },
        
        # Role requirements analysis
        "role_requirements": {
            "seniority_level": str,  # Junior, Mid, Senior, Lead, etc.
            "min_experience_years": float,
            "preferred_experience_years": float,
            "min_education": str,
            "preferred_education": str,
            "required_certifications": List[str],
            "management_responsibilities": bool,
            "team_size": int  # If management role
        },
        
        # Competitive analysis
        "market_analysis": {
            "similar_roles": List[str],
            "average_salary_range": Dict[str, float],  # {"min": 80000, "max": 120000}
            "demand_level": str,  # High, Medium, Low
            "supply_level": str,  # High, Medium, Low
            "trending_skills": List[str]
        },
        
        # AI-generated insights
        "ai_insights": {
            "role_summary": str,
            "key_differentiators": List[str],
            "suggested_interview_questions": List[Dict[str, str]],  # [{"question": "...", "purpose": "..."}]
            "evaluation_criteria": List[Dict[str, Any]],
            "candidate_sourcing_suggestions": List[str],
            "role_challenges": List[str],
            "success_indicators": List[str]
        },
        
        # Generated at timestamp
        "generated_at": datetime,
        "updated_at": datetime
    }
    
    # Create index on job_id for fast lookups
    db.jd_insights.create_index([("job_id", ASCENDING)])
    db.jd_insights.create_index([("title", "text")])
    
    return jd_insights

def create_decision_making_insights_collection():
    """Schema for storing comprehensive decision-making insights"""
    decision_making_insights = {
        "decision_id": int,
        "job_id": int,
        "candidate_id": int,
        "resume_id": int,
        "created_by": int,  # User ID who initiated the decision
        "decision_date": datetime,
        
        # Decision context
        "decision_context": {
            "stage": str,  # "Initial Screening", "Technical Interview", "Final Round", etc.
            "position": str,
            "department": str,
            "urgency_level": str,  # "Low", "Medium", "High"
            "hiring_goals": List[str]
        },
        
        # Candidate assessment
        "candidate_assessment": {
            "resume_score": float,
            "interview_scores": List[Dict[str, Any]],  # Multiple interview scores
            "skill_match": float,
            "experience_relevance": float,
            "cultural_fit": float,
            "overall_rating": float
        },
        
        # Decision factors
        "decision_factors": {
            "technical_competence": {
                "weight": float,
                "score": float,
                "justification": str
            },
            "experience": {
                "weight": float,
                "score": float,
                "justification": str
            },
            "cultural_fit": {
                "weight": float,
                "score": float,
                "justification": str
            },
            "communication_skills": {
                "weight": float,
                "score": float,
                "justification": str
            },
            "growth_potential": {
                "weight": float,
                "score": float,
                "justification": str
            },
            "additional_factors": List[Dict[str, Any]]
        },
        
        # Decision recommendation
        "recommendation": {
            "decision": str,  # "Hire", "Reject", "Hold", "Additional Interview"
            "confidence": float,  # 0-100
            "justification": str,
            "considerations": List[str],
            "risks": List[str],
            "next_steps": List[str]
        },
        
        # Comparison with other candidates
        "comparative_analysis": {
            "candidate_ranking": int,  # Rank among all candidates
            "percentile": float,  # Percentile among all candidates
            "strengths_vs_others": List[str],
            "weaknesses_vs_others": List[str],
            "unique_value_proposition": str
        },
        
        # AI insights
        "ai_insights": {
            "bias_detection": {
                "detected_biases": List[str],
                "mitigation_suggestions": List[str]
            },
            "decision_quality": float,  # 0-100
            "confidence_score": float,  # 0-100
            "alternative_perspectives": List[str],
            "long_term_fit_prediction": float  # 0-100
        },
        
        # Decision status
        "status": str,  # "Draft", "Pending", "Approved", "Rejected"
        "approvers": List[int],  # User IDs of approvers
        "comments": List[Dict[str, Any]],  # Comments from reviewers
        
        # Original data from resume analysis
        "resume_data": {
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
            }
        },
        
        # Timestamps
        "created_at": datetime,
        "updated_at": datetime,
        "generated_at": datetime
    }
    
    # Create indexes for efficient querying
    db.decision_making_insights.create_index([("decision_id", ASCENDING)])
    db.decision_making_insights.create_index([("job_id", ASCENDING)])
    db.decision_making_insights.create_index([("candidate_id", ASCENDING)])
    db.decision_making_insights.create_index([("resume_id", ASCENDING)])
    db.decision_making_insights.create_index([("created_at", ASCENDING)])
    
    return decision_making_insights

def create_candidate_evaluation_collection():
    """Enhanced schema for storing candidate evaluations after interviews"""
    candidate_eval = {
        "evaluation_id": int,  # Unique identifier for this evaluation
        "candidate_id": int,  # Reference to SQL candidate_id
        "job_id": int,  # Reference to SQL job_id
        "interview_id": int,  # Reference to the interview session
        "evaluator_id": int,  # User who conducted the interview (if applicable)
        "evaluation_date": datetime,
        
        # Overall scores
        "overall_scores": {
            "total_score": float,  # 0-100 overall score
            "recommendation": str,  # "Hire", "Reject", "Consider"
            "match_percentage": float,  # How well candidate matches JD
            "confidence_score": float  # AI confidence in evaluation
        },
        
        # Detailed scoring categories
        "category_scores": {
            "technical_skills": {
                "score": float,  # 0-100
                "strengths": List[str],
                "weaknesses": List[str],
                "detailed_skills": Dict[str, float]  # Individual skill scores
            },
            "experience": {
                "score": float,
                "relevance": float,
                "depth": float,
                "breadth": float,
                "achievements": List[str]
            },
            "communication": {
                "score": float,
                "clarity": float,
                "articulation": float,
                "listening": float,
                "non_verbal": float
            },
            "problem_solving": {
                "score": float,
                "approach": float,
                "creativity": float,
                "analytical_thinking": float
            },
            "cultural_fit": {
                "score": float,
                "alignment": float,
                "adaptability": float,
                "teamwork": float
            }
        },
        
        # Question-by-question analysis
        "question_analysis": List[Dict[str, Any]],
        
        # AI-generated feedback
        "ai_feedback": {
            "summary": str,  # Overall evaluation summary
            "strengths": List[str],  # Key strengths identified
            "areas_for_improvement": List[str],
            "hiring_recommendation": str,  # Detailed recommendation
            "fit_analysis": str,  # Analysis of fit for the role
            "suggested_interview_questions": List[str]  # For follow-up interviews
        },
        
        # Skill assessment against job requirements
        "skill_assessment": {
            "required_skills": List[str],
            "matched_skills": List[str],
            "missing_skills": List[str],
            "skill_scores": Dict[str, float],
            "skill_gap_analysis": str
        },
        
        # Metadata
        "evaluation_type": str,  # "AI", "Human", "Hybrid"
        "evaluation_method": str,  # "Video", "Audio", "Text"
        "evaluation_duration": float,  # In minutes
        "notes": str,  # Additional notes
        "status": str,  # "Draft", "Completed", "Reviewed"
        
        # Timestamps
        "created_at": datetime,
        "updated_at": datetime
    }
    # Create indexes for fast lookups
    db.candidate_evaluations.create_index([("candidate_id", ASCENDING)])
    db.candidate_evaluations.create_index([("evaluation_id", ASCENDING)])
    db.candidate_evaluations.create_index([("job_id", ASCENDING)])
    db.candidate_evaluations.create_index([("interview_id", ASCENDING)])
    

    return candidate_eval

def create_interview_transcription_collection():
    interview_transcription = {
        "interview_id": int,
        "candidate_id": int,
        "job_id": int,
        "resume_id": int,
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


def create_qa_scoring_rubrics_collection():
    """Schema for storing Q/A scoring rubrics and mapping criteria"""
    qa_scoring_rubrics = {
        "rubric_id": int,
        "job_id": int,  # Optional, for job-specific rubrics
        "name": str,
        "description": str,
        "question_type": str,  # "Technical", "Behavioral", "Coding", "Domain-specific"
        
        # Scoring criteria
        "scoring_criteria": List[Dict[str, Any]],  # List of criteria with weights
        
        # Score mapping
        "score_mapping": {
            "excellent": {
                "min_score": float,
                "max_score": float,
                "description": str
            },
            "good": {
                "min_score": float,
                "max_score": float,
                "description": str
            },
            "average": {
                "min_score": float,
                "max_score": float,
                "description": str
            },
            "below_average": {
                "min_score": float,
                "max_score": float,
                "description": str
            },
            "poor": {
                "min_score": float,
                "max_score": float,
                "description": str
            }
        },
        
        # Weighting system
        "question_weights": Dict[str, float],  # Weights for different question aspects
        
        # Created/updated timestamps
        "created_at": datetime,
        "updated_at": datetime
    }
    
    db.qa_scoring_rubrics.create_index([("rubric_id", ASCENDING)])
    db.qa_scoring_rubrics.create_index([("job_id", ASCENDING)])
    
    return qa_scoring_rubrics

def create_coding_evaluation_collection():
    """Schema for storing coding-specific evaluations"""
    coding_evaluation = {
        "evaluation_id": int,
        "candidate_id": int,
        "job_id": int,
        "question_id": int,
        
        # Code submission
        "code_submission": {
            "language": str,
            "code_text": str,
            "submission_time": datetime
        },
        
        # Execution results
        "execution_results": {
            "status": str,  # "Success", "Error", "Timeout"
            "output": str,
            "runtime": float,  # in milliseconds
            "memory_usage": float,  # in KB
            "test_cases_passed": int,
            "total_test_cases": int
        },
        
        # Code quality metrics
        "code_quality": {
            "correctness": float,  # 0-100
            "efficiency": float,  # 0-100
            "code_style": float,  # 0-100
            "readability": float,  # 0-100
            "maintainability": float,  # 0-100
            "error_handling": float  # 0-100
        },
        
        # AI analysis
        "ai_analysis": {
            "strengths": List[str],
            "weaknesses": List[str],
            "suggestions": List[str],
            "alternative_approaches": List[str],
            "complexity_analysis": str
        },
        
        # Overall score
        "overall_score": float,  # 0-100
        
        # Timestamps
        "created_at": datetime,
        "updated_at": datetime
    }
    
    db.coding_evaluations.create_index([("evaluation_id", ASCENDING)])
    db.coding_evaluations.create_index([("candidate_id", ASCENDING)])
    db.coding_evaluations.create_index([("job_id", ASCENDING)])
    
    return coding_evaluation

def create_candidate_comparison_collection():
    """Schema for storing candidate comparison data"""
    candidate_comparison = {
        "comparison_id": int,
        "job_id": int,
        "created_by": int,  # User ID
        "comparison_date": datetime,
        
        # Candidates being compared
        "candidates": List[Dict[str, Any]],  # List of candidate summaries
        
        # Comparison metrics
        "comparison_metrics": {
            "technical_skills": Dict[int, float],  # candidate_id: score
            "communication": Dict[int, float],
            "problem_solving": Dict[int, float],
            "experience_relevance": Dict[int, float],
            "cultural_fit": Dict[int, float],
            "overall_ranking": Dict[int, int]  # candidate_id: rank
        },
        
        # Question-by-question comparison
        "question_comparisons": List[Dict[str, Any]],  # Detailed comparison by question
        
        # AI insights
        "ai_insights": {
            "strongest_candidate": int,  # candidate_id
            "justification": str,
            "candidate_strengths": Dict[int, List[str]],  # candidate_id: strengths
            "candidate_weaknesses": Dict[int, List[str]],  # candidate_id: weaknesses
            "hiring_recommendations": Dict[int, str]  # candidate_id: recommendation
        },
        
        # Timestamps
        "created_at": datetime,
        "updated_at": datetime
    }
    
    db.candidate_comparisons.create_index([("comparison_id", ASCENDING)])
    db.candidate_comparisons.create_index([("job_id", ASCENDING)])
    
    return candidate_comparison

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
        "job_descriptions": create_job_description_collection(),
        "jd_insights": create_jd_insights_collection(),
        "candidate_evaluations": create_candidate_evaluation_collection(),
        "decision_making_insights": create_decision_making_insights_collection(),
        "interview_transcriptions": create_interview_transcription_collection(),
        "ai_generated_questions": create_ai_questions_collection(),
        "resume_insights": create_resume_insights_collection(),
        "qa_scoring_rubrics": create_qa_scoring_rubrics_collection(),
        "coding_evaluations": create_coding_evaluation_collection(),
        "candidate_comparisons": create_candidate_comparison_collection()
    }

    print("\nInitializing MongoDB Collections...")
    for name, schema in collections.items():
        print(f"✓ Initialized {name} collection")

    return collections


# Create all collections when module is imported
MONGODB_SCHEMAS = initialize_mongodb_collections()
