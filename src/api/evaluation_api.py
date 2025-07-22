from fastapi import APIRouter, HTTPException
import os
from dotenv import load_dotenv
from ..models.evaluation_models import InterviewInput, EvaluationResult
from ..services.spark_api import SparkAPI
from ..services.evaluation_engine import EvaluationEngine
from ..services.chart_generator import RadarChartGenerator

# 加载环境变量
load_dotenv()

# 创建路由器
router = APIRouter(prefix="/api/evaluation", tags=["evaluation"])

# 初始化服务 - 延迟初始化避免启动时的配置错误
spark_api = None
evaluation_engine = None
chart_generator = RadarChartGenerator()

def get_spark_api():
    global spark_api, evaluation_engine
    if spark_api is None:
        try:
            spark_api = SparkAPI(
                app_id=os.getenv("SPARK_APP_ID"),
                api_key=os.getenv("SPARK_API_KEY"),
                api_secret=os.getenv("SPARK_API_SECRET")
            )
            evaluation_engine = EvaluationEngine(spark_api)
        except ValueError as e:
            raise HTTPException(status_code=500, detail=str(e))
    return spark_api, evaluation_engine

@router.post("/analyze", response_model=EvaluationResult)
async def analyze_interview(input_data: InterviewInput):
    """
    分析面试数据并生成六维评估结果
    """
    try:
        # 获取初始化的服务
        _, engine = get_spark_api()
        
        # 生成六维评分
        scores = engine.generate_six_dimension_scores(input_data)
        
        # 生成雷达图
        radar_chart_base64 = chart_generator.generate_radar_chart(scores)
        
        # 生成总结和建议
        summary, recommendations = engine.generate_summary_and_recommendations(input_data, scores)
        
        return EvaluationResult(
            scores=scores,
            radar_chart_base64=radar_chart_base64,
            summary=summary,
            recommendations=recommendations
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"评估过程中发生错误: {str(e)}")

@router.get("/health")
async def health_check():
    """
    健康检查接口
    """
    return {"status": "healthy", "message": "Interview evaluation API is running"}