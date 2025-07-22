from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.evaluation_api import router as evaluation_router
import uvicorn
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建FastAPI应用
app = FastAPI(
    title="Interview Evaluation System",
    description="基于讯飞星火API的面试评估六维图系统",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加路由
app.include_router(evaluation_router)

@app.get("/")
async def root():
    return {
        "message": "Interview Evaluation System API", 
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True
    )