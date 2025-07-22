# Interview Evaluation System

基于讯飞星火API的面试评估六维图系统

## 功能特点

- 🤖 **智能评估**: 使用讯飞星火大模型分析面试数据
- 📊 **六维分析**: 从技能匹配、沟通表达、情绪稳定、专业素养、逻辑思维、学习潜力六个维度评估
- 📈 **可视化图表**: 生成直观的雷达图展示评估结果
- 🔧 **RESTful API**: 提供标准的HTTP接口，易于集成

## 六维评估体系

1. **技能匹配度** - 基于简历岗位匹配度分析
2. **沟通表达力** - 基于问答对话质量分析  
3. **情绪稳定性** - 基于语音情感分析结果
4. **专业素养** - 基于肢体语言分析结果
5. **逻辑思维** - 基于问答逻辑性分析
6. **学习潜力** - 综合各项数据评估

## 安装部署

### 1. 环境要求
- Python 3.8+
- pip

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境变量
复制 `.env.example` 为 `.env` 并填入你的讯飞星火API配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：
```
SPARK_APP_ID=your_app_id
SPARK_API_KEY=your_api_key
SPARK_API_SECRET=your_api_secret
HOST=0.0.0.0
PORT=8000
```

### 4. 运行服务
```bash
python main.py
```

服务将在 `http://localhost:8000` 启动。

## API 使用

### 健康检查
```bash
GET /api/evaluation/health
```

### 面试评估
```bash
POST /api/evaluation/analyze
```

请求体示例：
```json
{
  "resume_match_score": 85.0,
  "interview_qa_pairs": [
    {
      "question": "请介绍一下你的项目经验",
      "answer": "我参与开发过多个Web应用项目..."
    }
  ],
  "voice_emotion_analysis": {
    "positive": 0.7,
    "neutral": 0.2,
    "negative": 0.1
  },
  "body_language_analysis": {
    "confidence": 0.8,
    "engagement": 0.75,
    "nervousness": 0.2
  }
}
```

响应示例：
```json
{
  "scores": {
    "skill_match": 85.0,
    "communication": 78.5,
    "emotional_stability": 82.0,
    "professionalism": 80.0,
    "logical_thinking": 75.0,
    "learning_potential": 83.0
  },
  "radar_chart_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "summary": "面试者综合表现良好，技能匹配度较高...",
  "recommendations": [
    "建议加强逻辑表达能力",
    "可以进一步提升专业技能深度"
  ]
}
```

## 在线文档

启动服务后，访问 `http://localhost:8000/docs` 查看交互式API文档。

## 项目结构

```
interview-evaluation-system/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   └── evaluation_api.py      # API路由
│   ├── models/
│   │   ├── __init__.py
│   │   └── evaluation_models.py   # 数据模型
│   ├── services/
│   │   ├── __init__.py
│   │   ├── spark_api.py           # 星火API调用
│   │   ├── evaluation_engine.py   # 评估引擎
│   │   └── chart_generator.py     # 图表生成
│   └── __init__.py
├── main.py                        # 主程序入口
├── requirements.txt               # 依赖包
├── .env.example                   # 环境变量示例
└── README.md                      # 项目说明
```

## 许可证

MIT License