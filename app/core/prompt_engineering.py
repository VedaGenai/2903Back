# qa_template = """Analyze this job description and extract the following information:

# 1. The job roles mentioned (at least one role must be extracted)
# 2. Required skills for each role and their importance (%)
# 3. Selection score weightage for each skill (%)
# 4. Rejection score weightage for each skill (%)
# 5. Skill rating out of 10 based on importance
# 6. Required achievements/certifications and their importance (%)
# 7. Required skilled activities (with experience) and their importance (%)

# Importance Score (Sum: 100% per category): Represents the relative priority of each item.
# Selection Score (Sum: 100%): Indicates how much having each item contributes to candidate selection.
# Rejection Score (Sum: 100%): Indicates how much lacking each item leads to candidate rejection.
# Rating: Score out of 10 calculated as (Importance × 10 ÷ highest importance percentage in that category)

# Format your response EXACTLY as follows with one blank line between each section:

# Role: [Role Name]
# Skills:
# - [Skill Name]: Importance: [X]% Selection Score: [Y]% Rejection Score: [Z]% Rating: [R]/10
# - [Next Skill]: Importance: [X]% Selection Score: [Y]% Rejection Score: [Z]% Rating: [R]/10

# Achievements/Certifications:
# - [Achievement/Cert Name]: Importance: [X]% Selection Score: [Y]% Rejection Score: [Z]% Rating: [R]/10
# - [Next Achievement/Cert]: Importance: [X]% Selection Score: [Y]% Rejection Score: [Z]% Rating: [R]/10

# Skilled Activities:
# - [Activity Name]: Importance: [X]% Selection Score: [Y]% Rejection Score: [Z]% Rating: [R]/10
# - [Next Activity]: Importance: [X]% Selection Score: [Y]% Rejection Score: [Z]% Rating: [R]/10

# Rules:
# - You MUST list ALL roles found in the text
# - Importance percentages should sum to 100% within each category (Skills, Achievements/Certifications, Skilled Activities)
# - Selection and Rejection scores should each sum to 100% across all items per role
# - Use exact numbers, not ranges
# - Each role MUST have at least one item in each category
# - MUST include Rating for each item
# - Numbers should be rounded to one decimal place

# Job Description:
# {context}"""

# class PromptEngineering:
#     @staticmethod
#     def get_analysis_template():
#         return qa_template

import random
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Your original detailed qa_template
qa_template = """Analyze this job description and extract the following information:

1. The job roles mentioned (at least one role must be extracted)
2. Required skills for each role and their importance (%)
3. Selection score weightage for each skill (%)
4. Rejection score weightage for each skill (%)
5. Skill rating out of 10 based on importance
6. Required achievements/certifications and their importance (%)
7. Required skilled activities (with experience) and their importance (%)

Importance Score (Sum: 100% per category): Represents the relative priority of each item.
Selection Score (Sum: 100%): Indicates how much having each item contributes to candidate selection.
Rejection Score (Sum: 100%): Indicates how much lacking each item leads to candidate rejection.
Rating: Score out of 10 calculated as (Importance × 10 ÷ highest importance percentage in that category)

Format your response EXACTLY as follows with one blank line between each section:

Role: [Role Name]
Skills:
- [Skill Name]: Importance: [X]% Selection Score: [Y]% Rejection Score: [Z]% Rating: [R]/10
- [Next Skill]: Importance: [X]% Selection Score: [Y]% Rejection Score: [Z]% Rating: [R]/10

Achievements/Certifications:
- [Achievement/Cert Name]: Importance: [X]% Selection Score: [Y]% Rejection Score: [Z]% Rating: [R]/10
- [Next Achievement/Cert]: Importance: [X]% Selection Score: [Y]% Rejection Score: [Z]% Rating: [R]/10

Skilled Activities:
- [Activity Name]: Importance: [X]% Selection Score: [Y]% Rejection Score: [Z]% Rating: [R]/10
- [Next Activity]: Importance: [X]% Selection Score: [Y]% Rejection Score: [Z]% Rating: [R]/10

Rules:
- You MUST list ALL roles found in the text
- Importance percentages should sum to 100% within each category (Skills, Achievements/Certifications, Skilled Activities)
- Selection and Rejection scores should each sum to 100% across all items per role
- Use exact numbers, not ranges
- Each role MUST have at least one item in each category
- MUST include Rating for each item
- Numbers should be rounded to one decimal place

Job Description:
{context}"""

class PromptEngineering:
    @staticmethod
    def get_analysis_template():
        return qa_template

def generate_dynamic_prompts(skills_data, count):
    """Generate dynamic prompts based on skills data."""
    if not skills_data:
        return "Please upload and analyze a job description first."
    
    prompts = []
    for role, categories in skills_data.items():
        for category_name, items in categories.items():
            for item_name, data in items.items():
                current_rating = float(data.get('rating', 0))
                current_importance = float(data.get('importance', 0))
                current_selection = float(data.get('selection_score', 0))
                current_rejection = float(data.get('rejection_score', 0))
                
                new_prompts = [
                    f"Update {item_name}'s rating from {current_rating:.1f} to {min(10, current_rating + 1):.1f}",
                    f"Change {item_name}'s importance from {current_importance:.1f}% to {min(100, current_importance + 5):.1f}%",
                    f"Set {item_name}'s selection score from {current_selection:.1f}% to {min(100, current_selection + 10):.1f}%",
                    f"Adjust {item_name}'s rejection score from {current_rejection:.1f}% to {min(100, current_rejection + 10):.1f}%"
                ]
                prompts.extend(new_prompts)
    
    selected_prompts = random.sample(prompts, min(len(prompts), count))
    return "\n".join(selected_prompts)
