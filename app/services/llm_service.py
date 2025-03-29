import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from functools import lru_cache
import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
from ..core.Config import GOOGLE_API_KEY, MODEL_NAME, MODEL_TEMPERATURE
from ..core.prompt_engineering import qa_template, generate_dynamic_prompts

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = ChatGoogleGenerativeAI(
            model=MODEL_NAME,
            google_api_key=GOOGLE_API_KEY,
            temperature=MODEL_TEMPERATURE
        )
        self.current_skills_data = {}

    @lru_cache(maxsize=32)
    def get_llm_chain(self):
        prompt = ChatPromptTemplate.from_template(qa_template)
        chain = prompt | self.model
        return chain

    async def process_job_description(self, text: str):
        try:
            with ThreadPoolExecutor() as executor:
                chain = self.get_llm_chain()
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    executor,
                    lambda: chain.invoke({"context": text})
                )
                roles, skills_data, content = self.parse_llm_response(response.content)
                self.current_skills_data = skills_data  # Store the current skills data
                selected_prompts = generate_dynamic_prompts(skills_data, count=5)
                return roles, skills_data, content, self.calculate_threshold_scores(skills_data), selected_prompts
        except Exception as e:
            logger.error(f"Error in process_job_description: {str(e)}")
            return [], {}, "", (0.0, 0.0), []

    async def process_custom_prompt(self, prompt: str):
        try:
            with ThreadPoolExecutor() as executor:
                custom_prompt_template = ChatPromptTemplate.from_template(
                    """Current Skills Data: {skills_data}
                    
                    Instruction: {prompt}
                    
                    Update the skills data according to the instruction and return in the following format:
                    Role: [Role Name]
                    Skills:
                    - [Skill Name]: Importance: [X]% Selection Score: [Y]% Rejection Score: [Z]% Rating: [R]/5
                    
                    Return the complete updated data maintaining the exact same structure."""
                )
                
                chain = custom_prompt_template | self.model
                
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    executor,
                    lambda: chain.invoke({
                        "skills_data": str(self.current_skills_data),
                        "prompt": prompt
                    })
                )
                
                _, updated_skills_data, _ = self.parse_llm_response(response.content)
                if not updated_skills_data:
                    raise ValueError("No valid skills data returned")
                
                self.current_skills_data = updated_skills_data
                return updated_skills_data

        except Exception as e:
            logger.error(f"Error in process_custom_prompt: {str(e)}")
            raise ValueError(f"Failed to process prompt: {str(e)}")

    def parse_llm_response(self, content: str):
        roles = []
        skills_data = {}
        
        sections = content.split("Role:")
        for section in sections[1:]:
            lines = section.strip().split("\n")
            role_name = lines[0].strip()
            roles.append(role_name)
            
            skills_data[role_name] = {
                "skills": {},
                "achievements": {},
                "activities": {}
            }
            
            current_category = None
            for line in lines[1:]:
                line = line.strip()
                if "Skills:" in line:
                    current_category = "skills"
                elif "Achievements/Certifications:" in line:
                    current_category = "achievements"
                elif "Skilled Activities:" in line:
                    current_category = "activities"
                elif line.startswith("-") and current_category:
                    try:
                        item_parts = line[1:].strip().split(":")
                        item_name = item_parts[0].strip()
                        metrics_text = ":".join(item_parts[1:])
                        
                        metrics_dict = {
                            "importance": 0.0,
                            "selection_score": 0.0,
                            "rejection_score": 0.0,
                            "rating": 0.0
                        }
                        
                        for metric in metrics_text.split("%"):
                            metric = metric.strip()
                            if "Importance" in metric:
                                value = metric.split("Importance:")[-1].strip()
                                metrics_dict["importance"] = float(value)
                            elif "Selection Score" in metric:
                                value = metric.split("Selection Score:")[-1].strip()
                                metrics_dict["selection_score"] = float(value)
                            elif "Rejection Score" in metric:
                                value = metric.split("Rejection Score:")[-1].strip()
                                metrics_dict["rejection_score"] = float(value)
                            elif "Rating" in metric:
                                value = metric.split("Rating:")[-1].strip().split("/")[0].strip()
                                metrics_dict["rating"] = float(value)
                        
                        skills_data[role_name][current_category][item_name] = metrics_dict
                    except (ValueError, IndexError) as e:
                        logger.debug(f"Skipping line due to parsing error: {line}")
                        continue
        
        return roles, skills_data, content

    def calculate_threshold_scores(self, skills_data):
        all_scores = []
        for role_data in skills_data.values():
            for category in ['skills', 'achievements', 'activities']:
                for skill_data in role_data[category].values():
                    score_entry = {
                        'selection': skill_data['selection_score'],
                        'rejection': skill_data['rejection_score'],
                        'importance': skill_data['importance']
                    }
                    if any(score_entry.values()):
                        all_scores.append(score_entry)
        
        if all_scores:
            selection_scores = [score['selection'] * score['importance'] / 100 for score in all_scores]
            rejection_scores = [score['rejection'] * score['importance'] / 100 for score in all_scores]
            return (
                max(0.1, sum(selection_scores) / len(selection_scores)),
                max(0.1, sum(rejection_scores) / len(rejection_scores))
            )
        return 0.5, 0.3