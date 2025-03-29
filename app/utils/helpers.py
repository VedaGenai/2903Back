from langchain_community.document_loaders import PyPDFLoader
import logging
from fastapi import HTTPException, UploadFile
import os
from ..core.Config import UPLOAD_DIR
import pandas as pd
from typing import Dict, List, Any, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tempfile
import PyPDF2
import io
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
import logging
from fastapi import HTTPException, UploadFile
import os
from ..core.Config import UPLOAD_DIR


logger = logging.getLogger(__name__)

async def process_pdf(file: UploadFile) -> str:
    try:
        content = await file.read()
        pdf_file = io.BytesIO(content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        if not text.strip():
            raise ValueError("No text content found in PDF")
            
        logger.info(f"Extracted text from PDF: {text[:200]}...")  # Log first 200 chars
        return text.strip()
        
    except Exception as e:
        logger.error(f"PDF processing error: {str(e)}")
        raise ValueError(f"Failed to process PDF: {str(e)}")

def handle_role_selection(roles: List[str], skills_data: Dict[str, Any]) -> Tuple[List, float, float, str]:
    try:
        processed_data = []
        
        for role in roles:
            if role in skills_data:
                role_data = skills_data[role]
                metrics = calculate_role_metrics(role_data)
                processed_data.append({
                    'role': role,
                    'skills': role_data,
                    'metrics': metrics
                })
        
        selection_threshold, rejection_threshold = calculate_thresholds(processed_data)
        message = f"Successfully processed {len(processed_data)} roles"
        return processed_data, selection_threshold, rejection_threshold, message
    
    except Exception as e:
        logger.error(f"Error in handle_role_selection: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def calculate_role_metrics(role_data: Dict[str, Any]) -> Dict[str, float]:
    total_items = len(role_data)
    return {
        'total_importance': sum(item['importance'] for item in role_data.values()),
        'avg_selection': sum(item['selection_score'] for item in role_data.values()) / total_items,
        'avg_rejection': sum(item['rejection_score'] for item in role_data.values()) / total_items,
        'avg_rating': sum(item['rating'] for item in role_data.values()) / total_items
    }

def calculate_thresholds(processed_data: List[Dict[str, Any]]) -> Tuple[float, float]:
    if not processed_data:
        return 75.0, 25.0
    
    selection_scores = []
    rejection_scores = []
    
    for role_data in processed_data:
        selection_scores.append(role_data['metrics']['avg_selection'])
        rejection_scores.append(role_data['metrics']['avg_rejection'])
    
    return round(np.mean(selection_scores), 2), round(np.mean(rejection_scores), 2)

def handle_rating_change(data: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], float, float, str]:
    try:
        updated_data = {}
        for item in data:
            role = item['role']
            if role not in updated_data:
                updated_data[role] = {
                    'skills': {},
                    'achievements_certifications': {},
                    'skilled_activities': {}
                }
            
            category = item['category']
            name = item['name']
            updated_data[role][category][name] = {
                'importance': item['importance'],
                'selection_score': item['selection_score'],
                'rejection_score': item['rejection_score'],
                'rating': item['rating']
            }
        
        selection_threshold, rejection_threshold = calculate_thresholds([
            {'metrics': calculate_role_metrics(role_data)} 
            for role_data in updated_data.values()
        ])
        
        return updated_data, selection_threshold, rejection_threshold, "Ratings updated successfully"
    except Exception as e:
        logger.error(f"Error updating ratings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def calculate_similarity_score(text1: str, text2: str) -> float:
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

def validate_percentages(data: Dict[str, Any]) -> bool:
    for role_data in data.values():
        for category_data in role_data.values():
            importance_sum = sum(item['importance'] for item in category_data.values())
            selection_sum = sum(item['selection_score'] for item in category_data.values())
            rejection_sum = sum(item['rejection_score'] for item in category_data.values())
            
            if not (99.0 <= importance_sum <= 101.0 and 
                    99.0 <= selection_sum <= 101.0 and 
                    99.0 <= rejection_sum <= 101.0):
                return False
    return True

logger = logging.getLogger(__name__)

async def process_pdf(file: UploadFile):
    try:
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        loader = PyPDFLoader(str(file_path))
        pages = loader.load()
        text = "\n".join([page.page_content for page in pages[:2]])
        
        os.remove(file_path)
        return " ".join(text.split())
    except Exception as e:
        logger.error(f"PDF processing error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing PDF")

def handle_role_selection(roles, skills_data):
    try:
        processed_data = []
        selection_threshold = 75.0
        rejection_threshold = 25.0
        
        for role in roles:
            if role in skills_data:
                role_skills = skills_data[role]
                skill_metrics = {
                    'role': role,
                    'skills': role_skills,
                    'metrics': {
                        'total_importance': sum(skill['importance'] for skill in role_skills.values()),
                        'avg_selection': sum(skill['selection_score'] for skill in role_skills.values()) / len(role_skills),
                        'avg_rejection': sum(skill['rejection_score'] for skill in role_skills.values()) / len(role_skills)
                    }
                }
                processed_data.append(skill_metrics)
        
        message = f"Successfully processed {len(processed_data)} roles"
        return processed_data, selection_threshold, rejection_threshold, message
    
    except Exception as e:
        logger.error(f"Error in handle_role_selection: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
