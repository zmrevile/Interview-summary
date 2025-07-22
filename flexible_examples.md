# 灵活输入格式示例

现在API支持以下几种灵活的输入方式：

## 1. 最简单输入（只提供文字描述）
```json
{
  "text_description": "面试者表现良好，技术能力不错，但沟通稍显紧张"
}
```

## 2. 部分数据输入
```json
{
  "resume_match_score": 80,
  "text_description": "Python开发工程师面试，有3年经验"
}
```

## 3. 自定义字段输入
```json
{
  "candidate_name": "张三",
  "position": "高级开发工程师", 
  "interview_duration": "45分钟",
  "interviewer_notes": "技术能力强，团队协作有待观察",
  "overall_impression": "positive"
}
```

## 4. 混合格式输入
```json
{
  "resume_match_score": 75,
  "interview_notes": "面试者回答问题逻辑清晰，但对某些技术细节不够深入",
  "strengths": ["沟通能力", "学习能力"],
  "weaknesses": ["技术深度", "项目经验"],
  "recommendation": "建议通过，但需要技术培训"
}
```

## 5. 完整格式输入（原格式仍然支持）
```json
{
  "resume_match_score": 85.0,
  "interview_qa_pairs": [
    {"question": "介绍项目经验", "answer": "我做过电商系统..."}
  ],
  "voice_emotion_analysis": {"confidence": 0.8, "nervousness": 0.3},
  "body_language_analysis": {"eye_contact": 0.9, "posture": 0.7}
}
```

所有字段都是可选的，系统会根据提供的信息智能评估！