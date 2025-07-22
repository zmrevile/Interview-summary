import json
from typing import Dict, List
from ..models.evaluation_models import InterviewInput, SixDimensionScore
from .spark_api import SparkAPI

class EvaluationEngine:
    def __init__(self, spark_api: SparkAPI):
        self.spark_api = spark_api
    
    def generate_six_dimension_scores(self, input_data: InterviewInput) -> SixDimensionScore:
        """
        基于输入数据生成六维评分
        """
        # 构建prompt
        system_prompt = """
        你是一个专业的面试评估专家。请根据提供的面试数据，从以下六个维度对面试者进行评分（0-100分）：
        1. 技能匹配度 (skill_match) - 基于简历岗位匹配度
        2. 沟通表达力 (communication) - 基于问答对话的表达能力
        3. 情绪稳定性 (emotional_stability) - 基于语音情感分析
        4. 专业素养 (professionalism) - 基于肢体语言分析和整体表现
        5. 逻辑思维 (logical_thinking) - 基于问答的逻辑性和条理性
        6. 学习潜力 (learning_potential) - 综合评估学习和适应能力

        请以JSON格式返回评分结果，格式如下：
        {
            "skill_match": 分数,
            "communication": 分数,
            "emotional_stability": 分数,
            "professionalism": 分数,
            "logical_thinking": 分数,
            "learning_potential": 分数
        }
        """
        
        # 构建用户输入 - 灵活处理各种输入格式
        user_input_parts = ["面试数据分析：\n"]
        
        # 1. 简历匹配度
        if input_data.resume_match_score:
            user_input_parts.append(f"1. 简历岗位匹配度：{input_data.resume_match_score}分")
        
        # 2. 问答对话
        if input_data.interview_qa_pairs:
            user_input_parts.append(f"2. 面试问答对话：\n{self._format_qa_pairs(input_data.interview_qa_pairs)}")
        
        # 3. 语音情感分析
        if input_data.voice_emotion_analysis:
            user_input_parts.append(f"3. 语音情感分析结果：\n{self._format_emotion_analysis(input_data.voice_emotion_analysis)}")
        
        # 4. 肢体语言分析
        if input_data.body_language_analysis:
            user_input_parts.append(f"4. 肢体语言分析结果：\n{self._format_body_analysis(input_data.body_language_analysis)}")
        
        # 5. 文字描述（新增）
        if input_data.text_description:
            user_input_parts.append(f"5. 面试情况描述：\n{input_data.text_description}")
        
        # 6. 处理额外字段
        extra_fields = []
        for key, value in input_data.__dict__.items():
            if key not in ['resume_match_score', 'interview_qa_pairs', 'voice_emotion_analysis', 'body_language_analysis', 'text_description']:
                extra_fields.append(f"{key}: {value}")
        
        if extra_fields:
            user_input_parts.append("6. 其他相关信息：\n" + "\n".join(extra_fields))
        
        user_input_parts.append("\n请根据以上数据进行六维评分分析。如果某些数据缺失，请根据现有信息合理推测。")
        
        user_input = "\n\n".join(user_input_parts)
        
        # 调用星火API
        response = self.spark_api.send_message(user_input, system_prompt)
        
        # 解析响应
        try:
            # 提取JSON部分
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            json_str = response[json_start:json_end]
            
            scores_dict = json.loads(json_str)
            
            return SixDimensionScore(
                skill_match=float(scores_dict.get('skill_match', 60)),
                communication=float(scores_dict.get('communication', 60)),
                emotional_stability=float(scores_dict.get('emotional_stability', 60)),
                professionalism=float(scores_dict.get('professionalism', 60)),
                logical_thinking=float(scores_dict.get('logical_thinking', 60)),
                learning_potential=float(scores_dict.get('learning_potential', 60))
            )
        except Exception as e:
            # 如果解析失败，返回默认分数
            return SixDimensionScore(
                skill_match=input_data.resume_match_score,
                communication=60.0,
                emotional_stability=60.0,
                professionalism=60.0,
                logical_thinking=60.0,
                learning_potential=60.0
            )
    
    def generate_summary_and_recommendations(self, input_data: InterviewInput, scores: SixDimensionScore) -> tuple[str, List[str]]:
        """
        生成评估总结和改进建议
        """
        system_prompt = """
        你是一个专业的HR顾问。基于面试者的六维评分，请提供：
        1. 一个简洁的总结评价（100字以内）
        2. 3-5条具体的改进建议
        
        请以JSON格式返回：
        {
            "summary": "总结评价",
            "recommendations": ["建议1", "建议2", "建议3"]
        }
        """
        
        user_input = f"""
        面试者六维评分：
        - 技能匹配度：{scores.skill_match}分
        - 沟通表达力：{scores.communication}分
        - 情绪稳定性：{scores.emotional_stability}分
        - 专业素养：{scores.professionalism}分
        - 逻辑思维：{scores.logical_thinking}分
        - 学习潜力：{scores.learning_potential}分
        
        请提供总结评价和改进建议。
        """
        
        try:
            response = self.spark_api.send_message(user_input, system_prompt)
            
            # 提取JSON部分
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            json_str = response[json_start:json_end]
            
            result = json.loads(json_str)
            
            return result.get('summary', '综合表现良好，有进步空间。'), result.get('recommendations', ['继续努力，保持学习'])
        except Exception:
            # 默认响应
            return "综合表现良好，有进步空间。", ["提升专业技能", "加强沟通表达", "保持学习热情"]
    
    def _format_qa_pairs(self, qa_pairs: List[Dict[str, str]]) -> str:
        """格式化问答对话"""
        formatted = []
        for i, qa in enumerate(qa_pairs, 1):
            formatted.append(f"Q{i}: {qa.get('question', '')}")
            formatted.append(f"A{i}: {qa.get('answer', '')}")
        return "\n".join(formatted)
    
    def _format_emotion_analysis(self, emotion_data: Dict[str, float]) -> str:
        """格式化情感分析结果"""
        formatted = []
        for emotion, score in emotion_data.items():
            formatted.append(f"{emotion}: {score}")
        return "\n".join(formatted)
    
    def _format_body_analysis(self, body_data: Dict[str, float]) -> str:
        """格式化肢体分析结果"""
        formatted = []
        for aspect, score in body_data.items():
            formatted.append(f"{aspect}: {score}")
        return "\n".join(formatted)