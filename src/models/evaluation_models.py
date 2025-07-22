from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any, Union

class InterviewInput(BaseModel):
    """面试输入数据模型 - 灵活输入格式"""
    resume_match_score: Optional[float] = Field(default=60.0, description="简历岗位匹配度")
    interview_qa_pairs: Optional[List[Dict[str, Any]]] = Field(default=[], description="面试问答对话")
    voice_emotion_analysis: Optional[Dict[str, Union[float, int, str]]] = Field(default={}, description="语音情感分析")
    body_language_analysis: Optional[Dict[str, Union[float, int, str]]] = Field(default={}, description="肢体语言分析")
    
    # 新增：允许用户直接输入文本描述
    text_description: Optional[str] = Field(default="", description="面试情况的文字描述")
    
    class Config:
        # 允许任意额外字段
        extra = "allow"

class SixDimensionScore(BaseModel):
    """六维评分模型"""
    skill_match: float  # 技能匹配度 (0-100)
    communication: float  # 沟通表达力 (0-100)
    emotional_stability: float  # 情绪稳定性 (0-100)
    professionalism: float  # 专业素养 (0-100)
    logical_thinking: float  # 逻辑思维 (0-100)
    learning_potential: float  # 学习潜力 (0-100)

class EvaluationResult(BaseModel):
    """评估结果模型"""
    scores: SixDimensionScore
    radar_chart_base64: str  # 六维雷达图的base64编码
    summary: str  # 评估总结
    recommendations: List[str]  # 改进建议