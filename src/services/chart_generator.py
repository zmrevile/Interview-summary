import matplotlib
matplotlib.use('Agg')  # 使用非GUI后端
import matplotlib.pyplot as plt
import numpy as np
import base64
import io
from typing import List
from ..models.evaluation_models import SixDimensionScore

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class RadarChartGenerator:
    def __init__(self):
        self.dimensions = [
            '技能匹配',
            '沟通表达',
            '情绪稳定',
            '专业素养', 
            '逻辑思维',
            '学习潜力'
        ]
    
    def generate_radar_chart(self, scores: SixDimensionScore) -> str:
        """
        生成六维雷达图并返回base64编码的图片
        """
        # 提取分数
        values = [
            scores.skill_match,
            scores.communication,
            scores.emotional_stability,
            scores.professionalism,
            scores.logical_thinking,
            scores.learning_potential
        ]
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        # 设置角度
        angles = np.linspace(0, 2 * np.pi, len(self.dimensions), endpoint=False).tolist()
        angles += angles[:1]  # 闭合图形
        values += values[:1]  # 闭合图形
        
        # 绘制雷达图
        ax.plot(angles, values, 'o-', linewidth=2, color='#1f77b4', label='面试者评分')
        ax.fill(angles, values, alpha=0.25, color='#1f77b4')
        
        # 设置坐标轴
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(self.dimensions, fontsize=12)
        ax.set_ylim(0, 100)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=10)
        ax.grid(True)
        
        # 添加标题
        plt.title('面试评估六维图', size=16, fontweight='bold', pad=20)
        
        # 在每个顶点显示分数
        for angle, value, dim in zip(angles[:-1], values[:-1], self.dimensions):
            ax.annotate(f'{value:.1f}', 
                       xy=(angle, value), 
                       xytext=(10, 10), 
                       textcoords='offset points',
                       fontsize=10,
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
        
        # 保存图形到内存
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        buffer.seek(0)
        
        # 转换为base64
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # 清理内存
        plt.close(fig)
        buffer.close()
        
        return f"data:image/png;base64,{image_base64}"
    
    def generate_comparison_chart(self, current_scores: SixDimensionScore, 
                                 benchmark_scores: SixDimensionScore = None) -> str:
        """
        生成对比雷达图（当前分数 vs 基准分数）
        """
        if benchmark_scores is None:
            # 默认基准分数（优秀标准）
            benchmark_values = [85, 85, 85, 85, 85, 85]
        else:
            benchmark_values = [
                benchmark_scores.skill_match,
                benchmark_scores.communication,
                benchmark_scores.emotional_stability,
                benchmark_scores.professionalism,
                benchmark_scores.logical_thinking,
                benchmark_scores.learning_potential
            ]
        
        current_values = [
            current_scores.skill_match,
            current_scores.communication,
            current_scores.emotional_stability,
            current_scores.professionalism,
            current_scores.logical_thinking,
            current_scores.learning_potential
        ]
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        # 设置角度
        angles = np.linspace(0, 2 * np.pi, len(self.dimensions), endpoint=False).tolist()
        angles += angles[:1]
        current_values += current_values[:1]
        benchmark_values += benchmark_values[:1]
        
        # 绘制雷达图
        ax.plot(angles, current_values, 'o-', linewidth=2, color='#1f77b4', label='当前评分')
        ax.fill(angles, current_values, alpha=0.25, color='#1f77b4')
        
        ax.plot(angles, benchmark_values, 'o-', linewidth=2, color='#ff7f0e', label='优秀基准')
        ax.fill(angles, benchmark_values, alpha=0.15, color='#ff7f0e')
        
        # 设置坐标轴
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(self.dimensions, fontsize=12)
        ax.set_ylim(0, 100)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=10)
        ax.grid(True)
        
        # 添加标题和图例
        plt.title('面试评估对比图', size=16, fontweight='bold', pad=20)
        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        
        # 保存图形到内存
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        buffer.seek(0)
        
        # 转换为base64
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # 清理内存
        plt.close(fig)
        buffer.close()
        
        return f"data:image/png;base64,{image_base64}"