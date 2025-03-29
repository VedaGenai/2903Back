# from pydantic import BaseModel
# from typing import List, Optional

# class EvaluationResult(BaseModel):
#     technical_score: int
#     clarity_score: int
#     completeness_score: int
#     overall_score: int
#     decision: str
#     strengths: str
#     improvements: str

# class AudioTranscription(BaseModel):
#     text: str
#     clarity: str
#     error: Optional[str] = None


#    #threshold 
# from pydantic import BaseModel
# from typing import List, Dict, Any, Optional

# class SkillWeightage(BaseModel):
#     importance: float
#     selection_score: float
#     rejection_score: float

# class RoleSkills(BaseModel):
#     skills: Dict[str, SkillWeightage]

# class JobAnalysisResponse(BaseModel):
#     roles: List[str]
#     skills_data: Dict[str, Dict[str, SkillWeightage]]
#     data: Dict[str, Any]

# class DashboardResponse(BaseModel):
#     status: str
#     message: str
#     dashboards: List[Any]
#     selection_threshold: float
#     rejection_threshold: float
#     number_of_dashboards: int = 1
  
