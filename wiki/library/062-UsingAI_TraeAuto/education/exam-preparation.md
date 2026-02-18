# AI考试准备

## 基本原理

### 技术方法
AI考试准备主要基于以下核心技术：

1. **智能内容分析**：分析考试大纲、历年真题和学习材料的内容结构
2. **个性化学习路径规划**：基于学习者的水平和目标，动态生成最佳学习路径
3. **自适应测试**：根据学习者的表现，动态调整测试难度和内容
4. **知识图谱构建**：将学科知识构建成知识图谱，展示知识点间的关联
5. **自然语言处理（NLP）**：处理和理解学习材料、考试题目和答案
6. **机器学习（ML）**：从学习者的行为数据中学习，优化学习体验
7. **计算机视觉（CV）**：处理图表、公式和图像类的考试内容
8. **语音识别（ASR）**：支持语音交互和口语考试准备

### 核心技术原理
AI考试准备的核心原理主要包括：

1. **学习者建模**：通过分析学习者的历史表现、学习行为和反馈，构建学习者模型
2. **内容建模**：将考试内容分解为知识点、技能点和难度级别，建立内容模型
3. **智能评估**：基于学习者的答题表现，准确评估其知识掌握程度
4. **学习路径优化**：使用强化学习等技术，持续优化学习路径和推荐策略
5. **记忆增强**：结合认知科学原理，设计最优的复习间隔和方式
6. **自适应测试生成**：根据学习者水平，自动生成适合的测试题目
7. **反馈机制**：提供即时、具体、个性化的学习反馈
8. **学习动机激发**：通过游戏化设计和激励机制，提高学习积极性

### 常用模型和库

1. **AI学习平台**
   - Quizlet (带有AI学习功能)
   - Khan Academy (个性化学习路径)
   - Coursera (自适应学习体验)
   - Duolingo (游戏化语言学习)
   - Quizizz (自适应测验)
   - EdX (在线学习平台)

2. **开发工具和库**
   - TensorFlow/PyTorch (深度学习框架)
   - scikit-learn (机器学习算法)
   - spaCy/NLTK (自然语言处理)
   - OpenAI API/Claude API等 (内容生成和理解)
   - NetworkX (知识图谱构建)
   - Pandas/NumPy (数据处理)
   - Django/Flask (Web应用开发)
   - React/Vue.js (前端界面开发)

## 应用场景

### 1. 标准化考试准备
帮助学习者准备各种标准化考试，如SAT、ACT、GRE、GMAT、雅思、托福等。

### 2. 学校考试复习
为学生提供校内考试的个性化复习方案和练习题。

### 3. 职业认证考试准备
辅助专业人士准备各种职业认证考试，如PMP、CFA、CPA等。

### 4. 语言学习评估
提供语言学习的测试、评估和反馈，帮助提高语言能力。

### 5. 技能测评
评估学习者的专业技能水平，提供针对性的学习建议。

### 6. 个性化学习计划
根据学习者的目标、水平和时间，制定个性化的学习计划。

### 7. 学习进度追踪
实时追踪学习进度，及时调整学习策略。

### 8. 模拟考试
提供逼真的模拟考试体验，帮助学习者熟悉考试环境和流程。

## 详细使用示例

### 基础AI考试准备系统示例

下面是一个使用Python和机器学习技术实现的基础AI考试准备系统示例：

```python
import os
import json
import random
import datetime
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from collections import defaultdict

class AIExamPrepSystem:
    def __init__(self, data_path="exam_data"):
        """初始化AI考试准备系统"""
        # 初始化数据路径
        self.data_path = data_path
        
        # 确保数据目录存在
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
            
        # 初始化题库和学习者数据
        self.question_bank = []
        self.learners = {}
        self.learning_paths = {}
        
        # 初始化文本处理工具
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
        # 加载已有数据
        self.load_question_bank()
        self.load_learners_data()
        self.load_learning_paths()
        
    def load_question_bank(self):
        """加载题库"""
        qb_file = os.path.join(self.data_path, "question_bank.json")
        if os.path.exists(qb_file):
            try:
                with open(qb_file, 'r', encoding='utf-8') as f:
                    self.question_bank = json.load(f)
                print(f"已加载题库，包含{len(self.question_bank)}道题目")
            except Exception as e:
                print(f"加载题库失败：{e}")
        else:
            print("题库文件不存在，创建新的题库")
            # 创建一些示例题目
            self._create_example_questions()
        
    def save_question_bank(self):
        """保存题库"""
        qb_file = os.path.join(self.data_path, "question_bank.json")
        try:
            with open(qb_file, 'w', encoding='utf-8') as f:
                json.dump(self.question_bank, f, ensure_ascii=False, indent=2)
            print(f"题库已保存，包含{len(self.question_bank)}道题目")
        except Exception as e:
            print(f"保存题库失败：{e}")
            
    def load_learners_data(self):
        """加载学习者数据"""
        learners_file = os.path.join(self.data_path, "learners.json")
        if os.path.exists(learners_file):
            try:
                with open(learners_file, 'r', encoding='utf-8') as f:
                    self.learners = json.load(f)
                print(f"已加载学习者数据，包含{len(self.learners)}名学习者")
            except Exception as e:
                print(f"加载学习者数据失败：{e}")
        else:
            print("学习者数据文件不存在，创建新的学习者数据")
            
    def save_learners_data(self):
        """保存学习者数据"""
        learners_file = os.path.join(self.data_path, "learners.json")
        try:
            with open(learners_file, 'w', encoding='utf-8') as f:
                json.dump(self.learners, f, ensure_ascii=False, indent=2)
            print(f"学习者数据已保存，包含{len(self.learners)}名学习者")
        except Exception as e:
            print(f"保存学习者数据失败：{e}")
            
    def load_learning_paths(self):
        """加载学习路径"""
        paths_file = os.path.join(self.data_path, "learning_paths.json")
        if os.path.exists(paths_file):
            try:
                with open(paths_file, 'r', encoding='utf-8') as f:
                    self.learning_paths = json.load(f)
                print(f"已加载学习路径，包含{len(self.learning_paths)}条路径")
            except Exception as e:
                print(f"加载学习路径失败：{e}")
        else:
            print("学习路径文件不存在，创建新的学习路径")
            
    def save_learning_paths(self):
        """保存学习路径"""
        paths_file = os.path.join(self.data_path, "learning_paths.json")
        try:
            with open(paths_file, 'w', encoding='utf-8') as f:
                json.dump(self.learning_paths, f, ensure_ascii=False, indent=2)
            print(f"学习路径已保存，包含{len(self.learning_paths)}条路径")
        except Exception as e:
            print(f"保存学习路径失败：{e}")
            
    def _create_example_questions(self):
        """创建示例题目"""
        example_questions = [
            {
                "id": "q001",
                "content": "Python中，以下哪个不是内置数据类型？",
                "options": ["list", "tuple", "array", "dictionary"],
                "correct_answer": "array",
                "explanation": "array不是Python的内置数据类型，它属于NumPy库。其他选项都是Python的内置数据类型。",
                "category": "Python编程",
                "subcategory": "数据类型",
                "difficulty": 1,
                "tags": ["Python", "数据类型", "基础"]
            },
            {
                "id": "q002",
                "content": "机器学习中，以下哪种算法属于无监督学习？",
                "options": ["线性回归", "决策树", "聚类", "随机森林"],
                "correct_answer": "聚类",
                "explanation": "聚类算法属于无监督学习，它不需要标签数据，而是根据数据的内在结构进行分组。",
                "category": "机器学习",
                "subcategory": "算法类型",
                "difficulty": 2,
                "tags": ["机器学习", "无监督学习", "聚类"]
            },
            {
                "id": "q003",
                "content": "深度学习中，卷积神经网络主要用于处理哪种类型的数据？",
                "options": ["文本数据", "图像数据", "时间序列数据", "结构化数据"],
                "correct_answer": "图像数据",
                "explanation": "卷积神经网络(CNN)特别适合处理图像数据，它能够有效捕捉图像的局部特征和空间结构。",
                "category": "深度学习",
                "subcategory": "神经网络",
                "difficulty": 2,
                "tags": ["深度学习", "CNN", "图像处理"]
            },
            {
                "id": "q004",
                "content": "自然语言处理中，以下哪个模型是基于Transformer架构的？",
                "options": ["BERT", "Word2Vec", "GloVe", "LSTM"],
                "correct_answer": "BERT",
                "explanation": "BERT模型是基于Transformer架构的预训练语言模型，在多种NLP任务上取得了显著的成果。",
                "category": "自然语言处理",
                "subcategory": "语言模型",
                "difficulty": 3,
                "tags": ["NLP", "Transformer", "预训练模型"]
            },
            {
                "id": "q005",
                "content": "数据科学中，以下哪个步骤通常在数据预处理之后？",
                "options": ["数据收集", "特征工程", "模型评估", "模型部署"],
                "correct_answer": "特征工程",
                "explanation": "数据科学的典型流程是：数据收集 -> 数据预处理 -> 特征工程 -> 模型训练 -> 模型评估 -> 模型部署。",
                "category": "数据科学",
                "subcategory": "工作流程",
                "difficulty": 2,
                "tags": ["数据科学", "工作流程", "特征工程"]
            }
        ]
        
        self.question_bank = example_questions
        self.save_question_bank()
        
    def add_learner(self, learner_id, name, email, goals=None, subjects=None):
        """添加新学习者"""
        # 创建学习者档案
        learner_profile = {
            "id": learner_id,
            "name": name,
            "email": email,
            "goals": goals or [],
            "subjects": subjects or [],
            "join_date": datetime.datetime.now().isoformat(),
            "last_active": datetime.datetime.now().isoformat(),
            "performance": {},  # 存储各题目的表现
            "knowledge_map": {},  # 存储知识点掌握情况
            "study_history": [],  # 存储学习历史
            "preferences": {}  # 存储学习偏好
        }
        
        # 添加到学习者数据
        self.learners[learner_id] = learner_profile
        
        # 保存学习者数据
        self.save_learners_data()
        
        # 为学习者生成初始学习路径
        self.generate_learning_path(learner_id)
        
        return learner_profile
        
    def add_question(self, content, options, correct_answer, explanation, category, subcategory, difficulty, tags=None):
        """添加新题目"""
        # 生成唯一ID
        question_id = f"q{len(self.question_bank) + 1:03d}"
        
        # 创建题目对象
        question = {
            "id": question_id,
            "content": content,
            "options": options,
            "correct_answer": correct_answer,
            "explanation": explanation,
            "category": category,
            "subcategory": subcategory,
            "difficulty": difficulty,
            "tags": tags or [],
            "added_date": datetime.datetime.now().isoformat(),
            "usage_count": 0,
            "correct_rate": 0.0
        }
        
        # 添加到题库
        self.question_bank.append(question)
        
        # 保存题库
        self.save_question_bank()
        
        return question
        
    def generate_practice_test(self, learner_id, category=None, difficulty=None, num_questions=10):
        """为学习者生成练习测试"""
        if learner_id not in self.learners:
            return None, "学习者不存在"
            
        # 获取学习者的知识掌握情况
        knowledge_map = self.learners[learner_id].get("knowledge_map", {})
        
        # 筛选符合条件的题目
        filtered_questions = []
        for question in self.question_bank:
            # 按类别筛选
            if category and question.get("category") != category:
                continue
                
            # 按难度筛选
            if difficulty is not None and question.get("difficulty") != difficulty:
                continue
                
            # 根据学习者的知识掌握情况进行智能筛选
            # 如果知识点掌握不好，增加该知识点题目的权重
            subcategory = question.get("subcategory")
            mastery_level = knowledge_map.get(subcategory, 1.0)  # 默认掌握程度为1.0（完全不了解）
            
            # 生成随机数，如果小于(1-mastery_level)，则添加该题目
            # 这样，掌握程度越低的知识点，被选中的概率越高
            if random.random() < (1 - mastery_level) * 0.8 + 0.2:  # 至少有20%的概率选中任何题目
                filtered_questions.append(question)
                
        # 如果筛选后的题目不足，补充其他题目
        if len(filtered_questions) < num_questions:
            # 收集未被筛选的题目
            remaining_questions = [q for q in self.question_bank if q not in filtered_questions]
            
            # 补充足够的题目
            needed = num_questions - len(filtered_questions)
            filtered_questions.extend(random.sample(remaining_questions, min(needed, len(remaining_questions))))
            
        # 随机选择指定数量的题目
        if len(filtered_questions) >= num_questions:
            test_questions = random.sample(filtered_questions, num_questions)
        else:
            test_questions = filtered_questions
            
        # 创建测试
        test_id = f"test_{learner_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        test = {
            "id": test_id,
            "learner_id": learner_id,
            "questions": [q["id"] for q in test_questions],
            "created_at": datetime.datetime.now().isoformat(),
            "completed_at": None,
            "answers": {},
            "score": None,
            "performance": {}
        }
        
        # 添加到学习者的学习历史
        self.learners[learner_id]["study_history"].append({
            "type": "test",
            "id": test_id,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
        # 保存学习者数据
        self.save_learners_data()
        
        # 返回测试题目和测试ID
        return test, test_questions
        
    def submit_test_answers(self, test_id, learner_id, answers):
        """提交测试答案"""
        if learner_id not in self.learners:
            return False, "学习者不存在"
            
        # 查找测试
        test = None
        for history_item in self.learners[learner_id]["study_history"]:
            if history_item["type"] == "test" and history_item["id"] == test_id:
                # 假设我们在实际应用中会有一个单独的测试存储系统
                # 这里简化处理，重新生成测试题目
                _, test_questions = self.generate_practice_test(learner_id, num_questions=len(answers))
                break
        
        if not test_questions:
            return False, "测试不存在或已过期"
            
        # 计算得分和评估表现
        correct_count = 0
        performance = {}
        knowledge_map = self.learners[learner_id].get("knowledge_map", {})
        
        for question_id, user_answer in answers.items():
            # 查找题目
            question = next((q for q in test_questions if q["id"] == question_id), None)
            if not question:
                continue
                
            # 检查答案是否正确
            is_correct = user_answer == question["correct_answer"]
            
            # 更新题目使用次数和正确率
            question["usage_count"] += 1
            # 简单的正确率计算（实际应用中需要更复杂的算法）
            if is_correct:
                correct_count += 1
                
            # 更新学习者的知识掌握情况
            subcategory = question.get("subcategory")
            if subcategory not in knowledge_map:
                knowledge_map[subcategory] = 0.0
                
            # 根据答题情况更新掌握程度
            # 正确回答增加掌握程度，错误回答降低掌握程度
            if is_correct:
                knowledge_map[subcategory] = min(1.0, knowledge_map[subcategory] + 0.1)
            else:
                knowledge_map[subcategory] = max(0.0, knowledge_map[subcategory] - 0.05)
                
            # 记录本题的表现
            performance[question_id] = {
                "is_correct": is_correct,
                "user_answer": user_answer,
                "correct_answer": question["correct_answer"],
                "explanation": question["explanation"],
                "difficulty": question["difficulty"],
                "category": question["category"],
                "subcategory": question["subcategory"]
            }
        
        # 计算总得分
        total_questions = len(answers)
        score = (correct_count / total_questions) * 100 if total_questions > 0 else 0
        
        # 更新学习者数据
        self.learners[learner_id]["knowledge_map"] = knowledge_map
        self.learners[learner_id]["last_active"] = datetime.datetime.now().isoformat()
        
        # 保存更新后的数据
        self.save_learners_data()
        self.save_question_bank()
        
        # 生成学习建议
        recommendations = self.generate_study_recommendations(learner_id)
        
        # 更新学习路径
        self.generate_learning_path(learner_id)
        
        return True, {
            "score": score,
            "correct_count": correct_count,
            "total_questions": total_questions,
            "performance": performance,
            "recommendations": recommendations
        }
        
    def generate_study_recommendations(self, learner_id):
        """生成学习建议"""
        if learner_id not in self.learners:
            return []
            
        # 获取学习者的知识掌握情况
        knowledge_map = self.learners[learner_id].get("knowledge_map", {})
        
        # 找出掌握程度较低的知识点
        weak_areas = [(subcategory, mastery) for subcategory, mastery in knowledge_map.items() if mastery < 0.6]
        
        # 按掌握程度排序（从低到高）
        weak_areas.sort(key=lambda x: x[1])
        
        # 为每个薄弱知识点生成建议
        recommendations = []
        for subcategory, mastery in weak_areas[:3]:  # 只取前3个最薄弱的知识点
            # 查找相关题目
            related_questions = [q for q in self.question_bank if q.get("subcategory") == subcategory]
            
            if related_questions:
                # 随机选择几道相关题目作为练习
                practice_questions = random.sample(related_questions, min(3, len(related_questions)))
                
                recommendations.append({
                    "area": subcategory,
                    "mastery_level": mastery,
                    "recommendation": f"加强对{subcategory}的学习",
                    "practice_questions": [q["id"] for q in practice_questions]
                })
        
        # 如果没有薄弱知识点，生成一般建议
        if not recommendations:
            recommendations.append({
                "area": "总体复习",
                "mastery_level": 1.0,
                "recommendation": "继续保持良好的学习状态，可以挑战更难的题目或扩展相关知识点的学习",
                "practice_questions": []
            })
            
        return recommendations
        
    def generate_learning_path(self, learner_id):
        """生成学习路径"""
        if learner_id not in self.learners:
            return None, "学习者不存在"
            
        learner = self.learners[learner_id]
        
        # 获取学习者的目标和学科
        goals = learner.get("goals", [])
        subjects = learner.get("subjects", [])
        
        # 获取学习者的知识掌握情况
        knowledge_map = learner.get("knowledge_map", {})
        
        # 生成学习路径
        learning_path = {
            "id": f"path_{learner_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            "learner_id": learner_id,
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
            "goals": goals,
            "subjects": subjects,
            "modules": []
        }
        
        # 根据知识点掌握情况，生成学习模块
        # 这里简化处理，实际应用中需要更复杂的算法和更多的数据
        
        # 按类别分组题目
        questions_by_category = defaultdict(list)
        for question in self.question_bank:
            category = question.get("category")
            questions_by_category[category].append(question)
            
        # 为每个类别生成学习模块
        for category, questions in questions_by_category.items():
            # 如果学习者指定了学科，只包含指定学科的内容
            if subjects and category not in subjects:
                continue
                
            # 计算该类别的总体掌握程度
            category_questions = [q for q in questions]
            if not category_questions:
                continue
                
            # 找出该类别下的所有子类别
            subcategories = set(q.get("subcategory") for q in category_questions)
            
            # 计算每个子类别的掌握程度
            subcategory_mastery = {}
            for subcat in subcategories:
                mastery = knowledge_map.get(subcat, 0.5)  # 默认掌握程度为0.5
                subcategory_mastery[subcat] = mastery
                
            # 按掌握程度排序子类别（从低到高）
            sorted_subcategories = sorted(subcategory_mastery.items(), key=lambda x: x[1])
            
            # 为该类别创建学习模块
            module = {
                "category": category,
                "priority": 1 if category in subjects else 2,  # 指定学科优先级更高
                "estimated_time_hours": len(category_questions) * 0.1,  # 估计学习时间
                "progress": 0.0,
                "submodules": []
            }
            
            # 为每个子类别创建子模块
            for subcat, mastery in sorted_subcategories:
                # 找出该子类别的题目
                subcat_questions = [q for q in category_questions if q.get("subcategory") == subcat]
                
                if subcat_questions:
                    # 根据掌握程度确定练习题目数量
                    num_practice = max(3, int(len(subcat_questions) * (1 - mastery)))  # 掌握程度越低，练习题目越多
                    practice_questions = random.sample(subcat_questions, min(num_practice, len(subcat_questions)))
                    
                    submodule = {
                        "subcategory": subcat,
                        "mastery_level": mastery,
                        "priority": 1 if mastery < 0.5 else 2,  # 掌握程度低的优先级更高
                        "practice_questions": [q["id"] for q in practice_questions],
                        "progress": 0.0
                    }
                    
                    module["submodules"].append(submodule)
                    
            # 添加模块到学习路径
            learning_path["modules"].append(module)
            
        # 按优先级排序模块
        learning_path["modules"].sort(key=lambda x: x["priority"])
        
        # 更新学习者的学习路径
        self.learning_paths[learner_id] = learning_path
        
        # 保存学习路径
        self.save_learning_paths()
        
        return learning_path
        
    def get_learner_progress(self, learner_id):
        """获取学习者进度"""
        if learner_id not in self.learners:
            return None, "学习者不存在"
            
        learner = self.learners[learner_id]
        
        # 计算总体进度
        total_questions = len(self.question_bank)
        attempted_questions = len(learner.get("performance", {}))
        progress_percentage = (attempted_questions / total_questions) * 100 if total_questions > 0 else 0
        
        # 计算知识点掌握情况统计
        knowledge_map = learner.get("knowledge_map", {})
        if knowledge_map:
            avg_mastery = sum(knowledge_map.values()) / len(knowledge_map)
            strong_areas = [subcat for subcat, mastery in knowledge_map.items() if mastery >= 0.8]
            weak_areas = [subcat for subcat, mastery in knowledge_map.items() if mastery < 0.5]
        else:
            avg_mastery = 0.0
            strong_areas = []
            weak_areas = []
            
        # 获取最近的测试成绩
        recent_tests = [item for item in learner.get("study_history", []) if item["type"] == "test"][-5:]
        recent_scores = []
        
        # 计算学习活跃度
        study_history = learner.get("study_history", [])
        if study_history:
            # 计算最近30天的学习次数
            thirty_days_ago = datetime.datetime.now() - datetime.timedelta(days=30)
            recent_study_count = sum(1 for item in study_history if datetime.datetime.fromisoformat(item["timestamp"]) > thirty_days_ago)
        else:
            recent_study_count = 0
            
        # 获取学习路径信息
        learning_path = self.learning_paths.get(learner_id, {})
        
        return {
            "learner_id": learner_id,
            "name": learner.get("name"),
            "overall_progress": progress_percentage,
            "avg_mastery_level": avg_mastery,
            "strong_areas": strong_areas,
            "weak_areas": weak_areas,
            "recent_test_count": len(recent_tests),
            "recent_study_count": recent_study_count,
            "learning_path": learning_path,
            "last_active": learner.get("last_active")
        }
        
    def search_questions(self, query, category=None, difficulty=None, limit=10):
        """搜索题目"""
        # 如果有查询关键词，使用向量相似度搜索
        if query:
            # 提取所有题目内容用于向量化
            question_texts = [q["content"] for q in self.question_bank]
            
            # 向量化题目内容
            tfidf_matrix = self.vectorizer.fit_transform(question_texts)
            
            # 向量化查询
            query_vector = self.vectorizer.transform([query])
            
            # 计算相似度
            similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
            
            # 获取相似度最高的题目索引
            top_indices = similarities.argsort()[-min(limit * 2, len(similarities)):][::-1]  # 取两倍数量以便后续筛选
            
            # 根据索引获取题目
            search_results = [self.question_bank[i] for i in top_indices]
        else:
            # 如果没有查询关键词，返回所有题目
            search_results = self.question_bank.copy()
            
        # 进一步筛选（按类别和难度）
        filtered_results = []
        for question in search_results:
            # 按类别筛选
            if category and question.get("category") != category:
                continue
                
            # 按难度筛选
            if difficulty is not None and question.get("difficulty") != difficulty:
                continue
                
            filtered_results.append(question)
            
            # 如果达到限制数量，停止筛选
            if len(filtered_results) >= limit:
                break
                
        return filtered_results

# 使用示例
if __name__ == "__main__":
    # 创建AI考试准备系统实例
    exam_prep_system = AIExamPrepSystem()
    
    # 添加学习者
    print("添加学习者示例：")
    learner = exam_prep_system.add_learner(
        learner_id="learner001",
        name="张三",
        email="zhangsan@example.com",
        goals=["通过Python认证考试", "掌握机器学习基础知识"],
        subjects=["Python编程", "机器学习"]
    )
    print(f"已添加学习者：{learner['name']} (ID: {learner['id']})")
    
    # 生成练习测试
    print("\n生成练习测试示例：")
    test_info, test_questions = exam_prep_system.generate_practice_test("learner001", category="Python编程", num_questions=3)
    print(f"已生成测试，ID: {test_info['id']}")
    print(f"测试包含{len(test_questions)}道题目：")
    for i, question in enumerate(test_questions, 1):
        print(f"{i}. {question['content']}")
        print(f"   选项: {', '.join(question['options'])}")
    
    # 模拟提交答案
    print("\n提交测试答案示例：")
    # 这里我们假设用户回答了部分题目正确，部分错误
    answers = {
        test_questions[0]["id"]: test_questions[0]["correct_answer"],  # 正确回答
        test_questions[1]["id"]: random.choice([opt for opt in test_questions[1]["options"] if opt != test_questions[1]["correct_answer"]]),  # 错误回答
        test_questions[2]["id"]: test_questions[2]["correct_answer"]  # 正确回答
    }
    
    success, result = exam_prep_system.submit_test_answers(test_info['id'], "learner001", answers)
    print(f"提交结果：{success}")
    print(f"测试得分：{result['score']:.2f}分 ({result['correct_count']}/{result['total_questions']} 正确)")
    
    # 查看学习建议
    print("\n学习建议示例：")
    recommendations = result.get("recommendations", [])
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['recommendation']} (掌握程度: {rec['mastery_level']:.2f})")
    
    # 获取学习者进度
    print("\n学习者进度示例：")
    progress = exam_prep_system.get_learner_progress("learner001")
    print(f"学习者：{progress['name']}")
    print(f"总体进度：{progress['overall_progress']:.2f}%")
    print(f"平均掌握程度：{progress['avg_mastery_level']:.2f}")
    print(f"优势领域：{', '.join(progress['strong_areas']) if progress['strong_areas'] else '无'}")
    print(f"薄弱领域：{', '.join(progress['weak_areas']) if progress['weak_areas'] else '无'}")
    
    # 搜索题目
    print("\n搜索题目示例：")
    search_results = exam_prep_system.search_questions("神经网络", limit=2)
    print(f"找到{len(search_results)}道相关题目：")
    for i, question in enumerate(search_results, 1):
        print(f"{i}. {question['content']}")
        print(f"   类别: {question['category']} > {question['subcategory']}")
        print(f"   难度: {question['difficulty']}")
    
    # 添加新题目
    print("\n添加新题目示例：")
    new_question = exam_prep_system.add_question(
        content="Python中，以下哪个语句用于捕获异常？",
        options=["try", "catch", "except", "finally"],
        correct_answer="except",
        explanation="在Python中，使用except语句来捕获并处理异常。try块包含可能引发异常的代码，except块用于处理异常。",
        category="Python编程",
        subcategory="异常处理",
        difficulty=1,
        tags=["Python", "异常处理", "基础"]
    )
    print(f"已添加新题目：{new_question['content']} (ID: {new_question['id']})")
    
    # 查看更新后的题库
    print(f"\n更新后的题库数量：{len(exam_prep_system.question_bank)}道题目")
```

### 高级AI考试准备系统示例

下面是一个更高级的AI考试准备系统示例，结合了深度学习、自然语言处理和个性化推荐技术：

```python
import os
import json
import random
import datetime
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Embedding, LSTM, GRU, Dropout, Input, concatenate
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
import spacy
import re
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

class AdvancedAIExamPrepSystem:
    def __init__(self, data_path="advanced_exam_data"):
        """初始化高级AI考试准备系统"""
        # 初始化数据路径
        self.data_path = data_path
        
        # 确保数据目录存在
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
            
        # 初始化题库和学习者数据
        self.question_bank = []
        self.learners = {}
        self.learning_paths = {}
        self.question_embeddings = None
        self.performance_model = None
        
        # 初始化文本处理工具
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
        try:
            # 加载spaCy模型用于高级文本处理
            self.nlp = spacy.load("en_core_web_lg")
        except:
            try:
                self.nlp = spacy.load("en_core_web_sm")
                print("警告：使用较小的spaCy模型，可能影响性能")
            except:
                print("警告：未能加载spaCy模型，部分功能可能受限")
                self.nlp = None
        
        # 初始化预训练语言模型（用于题目生成和解释）
        try:
            self.qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
            self.text_generation_pipeline = pipeline("text-generation", model="gpt2", max_length=100)
        except:
            print("警告：未能加载预训练语言模型，部分功能可能受限")
            self.qa_pipeline = None
            self.text_generation_pipeline = None
        
        # 加载已有数据
        self.load_question_bank()
        self.load_learners_data()
        self.load_learning_paths()
        
        # 初始化和训练性能预测模型
        self._initialize_performance_model()
        
    def load_question_bank(self):
        """加载题库"""
        qb_file = os.path.join(self.data_path, "advanced_question_bank.json")
        if os.path.exists(qb_file):
            try:
                with open(qb_file, 'r', encoding='utf-8') as f:
                    self.question_bank = json.load(f)
                print(f"已加载高级题库，包含{len(self.question_bank)}道题目")
                
                # 生成题目嵌入
                self._generate_question_embeddings()
            except Exception as e:
                print(f"加载题库失败：{e}")
        else:
            print("高级题库文件不存在，创建新的题库")
            # 创建一些示例题目
            self._create_advanced_example_questions()
        
    def save_question_bank(self):
        """保存题库"""
        qb_file = os.path.join(self.data_path, "advanced_question_bank.json")
        try:
            with open(qb_file, 'w', encoding='utf-8') as f:
                json.dump(self.question_bank, f, ensure_ascii=False, indent=2)
            print(f"高级题库已保存，包含{len(self.question_bank)}道题目")
        except Exception as e:
            print(f"保存题库失败：{e}")
            
    def load_learners_data(self):
        """加载学习者数据"""
        learners_file = os.path.join(self.data_path, "advanced_learners.json")
        if os.path.exists(learners_file):
            try:
                with open(learners_file, 'r', encoding='utf-8') as f:
                    self.learners = json.load(f)
                print(f"已加载高级学习者数据，包含{len(self.learners)}名学习者")
            except Exception as e:
                print(f"加载学习者数据失败：{e}")
        else:
            print("高级学习者数据文件不存在，创建新的学习者数据")
            
    def save_learners_data(self):
        """保存学习者数据"""
        learners_file = os.path.join(self.data_path, "advanced_learners.json")
        try:
            with open(learners_file, 'w', encoding='utf-8') as f:
                json.dump(self.learners, f, ensure_ascii=False, indent=2)
            print(f"高级学习者数据已保存，包含{len(self.learners)}名学习者")
        except Exception as e:
            print(f"保存学习者数据失败：{e}")
            
    def load_learning_paths(self):
        """加载学习路径"""
        paths_file = os.path.join(self.data_path, "advanced_learning_paths.json")
        if os.path.exists(paths_file):
            try:
                with open(paths_file, 'r', encoding='utf-8') as f:
                    self.learning_paths = json.load(f)
                print(f"已加载高级学习路径，包含{len(self.learning_paths)}条路径")
            except Exception as e:
                print(f"加载学习路径失败：{e}")
        else:
            print("高级学习路径文件不存在，创建新的学习路径")
            
    def save_learning_paths(self):
        """保存学习路径"""
        paths_file = os.path.join(self.data_path, "advanced_learning_paths.json")
        try:
            with open(paths_file, 'w', encoding='utf-8') as f:
                json.dump(self.learning_paths, f, ensure_ascii=False, indent=2)
            print(f"高级学习路径已保存，包含{len(self.learning_paths)}条路径")
        except Exception as e:
            print(f"保存学习路径失败：{e}")
            
    def _create_advanced_example_questions(self):
        """创建高级示例题目"""
        # 这里添加更丰富的示例题目，包括多选题、填空题等
        example_questions = [
            {
                "id": "aq001",
                "content": "以下哪些是Python的内置数据类型？（多选）",
                "type": "multiple_choice",
                "options": ["list", "tuple", "array", "dictionary", "DataFrame"],
                "correct_answers": ["list", "tuple", "dictionary"],
                "explanation": "list、tuple和dictionary是Python的内置数据类型。array属于NumPy库，DataFrame属于pandas库。",
                "category": "Python编程",
                "subcategory": "数据类型",
                "difficulty": 2,
                "tags": ["Python", "数据类型", "基础"],
                "estimated_time_seconds": 45,
                "keywords": ["Python", "数据类型", "内置", "list", "tuple", "dictionary"]
            },
            {
                "id": "aq002",
                "content": "在机器学习中，________算法是一种无监督学习方法，用于将相似的数据点分组到同一簇中。",
                "type": "fill_blank",
                "correct_answer": "聚类",
                "explanation": "聚类算法是一种无监督学习方法，它不需要标签数据，而是根据数据的内在结构将相似的数据点分组到同一簇中。常见的聚类算法包括K-means、层次聚类等。",
                "category": "机器学习",
                "subcategory": "算法类型",
                "difficulty": 2,
                "tags": ["机器学习", "无监督学习", "聚类"],
                "estimated_time_seconds": 30,
                "keywords": ["机器学习", "无监督学习", "聚类", "分组"]
            },
            {
                "id": "aq003",
                "content": "请简述卷积神经网络(CNN)的主要特点及其在图像处理中的优势。",
                "type": "short_answer",
                "expected_answer_key_points": [
                    "局部连接和权值共享",
                    "卷积层提取特征",
                    "池化层降低维度",
                    "能够捕捉图像的空间特征",
                    "参数共享减少模型复杂度"
                ],
                "explanation": "卷积神经网络(CNN)的主要特点包括局部连接、权值共享和池化操作。在图像处理中，CNN能够有效捕捉图像的局部特征和空间结构，同时通过参数共享大大减少了模型的参数量，提高了训练效率和模型性能。",
                "category": "深度学习",
                "subcategory": "神经网络",
                "difficulty": 4,
                "tags": ["深度学习", "CNN", "图像处理"],
                "estimated_time_seconds": 120,
                "keywords": ["卷积神经网络", "CNN", "图像处理", "局部连接", "权值共享"]
            },
            {
                "id": "aq004",
                "content": "以下关于Transformer模型的说法，正确的是：（单选）",
                "type": "single_choice",
                "options": [
                    "Transformer模型只能处理文本数据",
                    "Transformer模型完全依赖于循环神经网络结构",
                    "Transformer模型使用自注意力机制来捕捉序列中的长距离依赖",
                    "BERT是第一个使用Transformer架构的模型"
                ],
                "correct_answer": "Transformer模型使用自注意力机制来捕捉序列中的长距离依赖",
                "explanation": "Transformer模型的核心创新是自注意力机制，它能够有效地捕捉序列数据中的长距离依赖关系。Transformer不依赖于循环神经网络结构，适用于多种数据类型，而BERT并不是第一个使用Transformer架构的模型。",
                "category": "自然语言处理",
                "subcategory": "语言模型",
                "difficulty": 3,
                "tags": ["NLP", "Transformer", "自注意力机制"],
                "estimated_time_seconds": 60,
                "keywords": ["Transformer", "自注意力机制", "NLP", "BERT"]
            },
            {
                "id": "aq005",
                "content": "数据科学项目的典型工作流程包括哪些步骤？请按顺序排列。",
                "type": "ordering",
                "items": ["数据收集", "模型部署", "特征工程", "数据预处理", "模型训练", "模型评估"],
                "correct_order": ["数据收集", "数据预处理", "特征工程", "模型训练", "模型评估", "模型部署"],
                "explanation": "数据科学项目的典型工作流程是：首先收集相关数据，然后进行数据预处理（清洗、转换等），接着进行特征工程（提取和选择特征），然后训练模型，评估模型性能，最后将模型部署到生产环境中。",
                "category": "数据科学",
                "subcategory": "工作流程",
                "difficulty": 3,
                "tags": ["数据科学", "工作流程", "项目管理"],
                "estimated_time_seconds": 90,
                "keywords": ["数据科学", "工作流程", "数据收集", "特征工程", "模型训练"]
            }
        ]
        
        self.question_bank = example_questions
        self.save_question_bank()
        
        # 生成题目嵌入
        self._generate_question_embeddings()
        
    def _generate_question_embeddings(self):
        """生成题目的嵌入向量"""
        if not self.question_bank or self.nlp is None:
            self.question_embeddings = None
            return
            
        # 提取所有题目内容用于生成嵌入
        question_texts = [q["content"] for q in self.question_bank]
        
        # 使用spaCy生成嵌入向量
        self.question_embeddings = []
        for text in question_texts:
            doc = self.nlp(text[:10000])  # 限制处理的文本长度
            self.question_embeddings.append(doc.vector)
            
        # 转换为numpy数组
        self.question_embeddings = np.array(self.question_embeddings)
        
    def _initialize_performance_model(self):
        """初始化性能预测模型"""
        # 这里我们创建一个简单的神经网络模型用于性能预测
        # 实际应用中，这个模型会更复杂，并且需要大量的历史数据进行训练
        
        try:
            # 创建模型
            self.performance_model = Sequential([
                Dense(64, activation='relu', input_shape=(300,)),  # 假设输入是300维的嵌入向量
                Dropout(0.2),
                Dense(32, activation='relu'),
                Dropout(0.2),
                Dense(1, activation='sigmoid')  # 输出是0-1之间的概率
            ])
            
            # 编译模型
            self.performance_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
            
            print("性能预测模型已初始化")
        except Exception as e:
            print(f"初始化性能预测模型失败：{e}")
            self.performance_model = None
            
    def add_learner(self, learner_id, name, email, goals=None, subjects=None, prior_knowledge=None):
        """添加新学习者"""
        # 创建学习者档案
        learner_profile = {
            "id": learner_id,
            "name": name,
            "email": email,
            "goals": goals or [],
            "subjects": subjects or [],
            "prior_knowledge": prior_knowledge or {},
            "join_date": datetime.datetime.now().isoformat(),
            "last_active": datetime.datetime.now().isoformat(),
            "performance": {},  # 存储各题目的表现
            "knowledge_map": {},  # 存储知识点掌握情况
            "learning_behavior": {},  # 存储学习行为数据
            "study_history": [],  # 存储学习历史
            "preferences": {},  # 存储学习偏好
            "confidence_level": {},  # 存储各知识点的自信心水平
            "learning_style": "balanced"  # 学习风格：visual, auditory, kinesthetic, balanced
        }
        
        # 添加到学习者数据
        self.learners[learner_id] = learner_profile
        
        # 保存学习者数据
        self.save_learners_data()
        
        # 为学习者生成初始学习路径
        self.generate_personalized_learning_path(learner_id)
        
        return learner_profile
        
    def add_question(self, content, question_type, correct_answer, explanation, category, subcategory, difficulty, 
                     options=None, expected_answer_key_points=None, items=None, correct_order=None, 
                     tags=None, estimated_time_seconds=None, keywords=None):
        """添加新题目（支持多种题型）"""
        # 生成唯一ID
        question_id = f"aq{len(self.question_bank) + 1:03d}"
        
        # 创建题目对象
        question = {
            "id": question_id,
            "content": content,
            "type": question_type,
            "explanation": explanation,
            "category": category,
            "subcategory": subcategory,
            "difficulty": difficulty,
            "tags": tags or [],
            "added_date": datetime.datetime.now().isoformat(),
            "usage_count": 0,
            "correct_rate": 0.0,
            "estimated_time_seconds": estimated_time_seconds or 60,
            "keywords": keywords or []
        }
        
        # 根据题型添加相应的字段
        if question_type == "single_choice" or question_type == "multiple_choice":
            question["options"] = options or []
            if question_type == "single_choice":
                question["correct_answer"] = correct_answer
            else:
                question["correct_answers"] = correct_answer
        elif question_type == "fill_blank" or question_type == "matching":
            question["correct_answer"] = correct_answer
        elif question_type == "short_answer" or question_type == "essay":
            question["expected_answer_key_points"] = expected_answer_key_points or []
        elif question_type == "ordering":
            question["items"] = items or []
            question["correct_order"] = correct_order or []
        
        # 添加到题库
        self.question_bank.append(question)
        
        # 重新生成题目嵌入
        self._generate_question_embeddings()
        
        # 保存题库
        self.save_question_bank()
        
        return question
        
    def generate_personalized_practice_test(self, learner_id, category=None, difficulty=None, 
                                           num_questions=10, adaptive=True):
        """为学习者生成个性化练习测试"""
        if learner_id not in self.learners:
            return None, "学习者不存在"
            
        learner = self.learners[learner_id]
        
        # 获取学习者的知识掌握情况
        knowledge_map = learner.get("knowledge_map", {})
        learning_behavior = learner.get("learning_behavior", {})
        
        # 筛选符合条件的题目
        filtered_questions = []
        
        if adaptive and self.performance_model is not None and self.question_embeddings is not None:
            # 使用自适应方法选择题目（基于性能预测模型）
            candidate_questions = []
            
            # 首先筛选基本条件
            for i, question in enumerate(self.question_bank):
                # 按类别筛选
                if category and question.get("category") != category:
                    continue
                    
                # 按难度筛选
                if difficulty is not None and question.get("difficulty") != difficulty:
                    continue
                    
                candidate_questions.append((i, question))
                
            # 如果有候选题目，使用模型预测学习者的表现
            if candidate_questions:
                question_indices, questions = zip(*candidate_questions)
                
                # 获取候选题目的嵌入
                candidate_embeddings = self.question_embeddings[list(question_indices)]
                
                # 使用模型预测（这里简化处理，实际应用中需要更复杂的学习者表示）
                try:
                    # 假设我们使用一个简化的学习者表示
                    # 实际应用中，应该使用更复杂的学习者特征向量
                    predictions = self.performance_model.predict(candidate_embeddings)
                    
                    # 选择预测难度适中的题目（预测正确率在0.3-0.7之间）
                    for i, (probability, question) in enumerate(zip(predictions, questions)):
                        # 结合知识掌握情况进行调整
                        subcategory = question.get("subcategory")
                        mastery_level = knowledge_map.get(subcategory, 0.5)
                        
                        # 调整预测概率
                        adjusted_probability = probability[0] * 0.5 + mastery_level * 0.5
                        
                        # 选择难度适中的题目（既不过于简单，也不过于困难）
                        if 0.3 <= adjusted_probability <= 0.7:
                            filtered_questions.append(question)
                except Exception as e:
                    print(f"使用性能预测模型失败：{e}")
                    # 回退到基础方法
                    filtered_questions = list(questions)
        else:
            # 使用基础方法选择题目
            for question in self.question_bank:
                # 按类别筛选
                if category and question.get("category") != category:
                    continue
                    
                # 按难度筛选
                if difficulty is not None and question.get("difficulty") != difficulty:
                    continue
                    
                # 根据学习者的知识掌握情况进行筛选
                subcategory = question.get("subcategory")
                mastery_level = knowledge_map.get(subcategory, 0.5)
                
                # 生成随机数，如果小于(1-mastery_level)，则添加该题目
                if random.random() < (1 - mastery_level) * 0.8 + 0.2:
                    filtered_questions.append(question)
                    
        # 如果筛选后的题目不足，补充其他题目
        if len(filtered_questions) < num_questions:
            # 收集未被筛选的题目
            remaining_questions = [q for q in self.question_bank if q not in filtered_questions]
            
            # 补充足够的题目
            needed = num_questions - len(filtered_questions)
            filtered_questions.extend(random.sample(remaining_questions, min(needed, len(remaining_questions))))
            
        # 随机选择指定数量的题目
        if len(filtered_questions) >= num_questions:
            test_questions = random.sample(filtered_questions, num_questions)
        else:
            test_questions = filtered_questions
            
        # 创建测试
        test_id = f"advanced_test_{learner_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        test = {
            "id": test_id,
            "learner_id": learner_id,
            "questions": [q["id"] for q in test_questions],
            "created_at": datetime.datetime.now().isoformat(),
            "completed_at": None,
            "answers": {},
            "score": None,
            "performance": {},
            "estimated_time_minutes": sum(q.get("estimated_time_seconds", 60) for q in test_questions) / 60
        }
        
        # 添加到学习者的学习历史
        learner["study_history"].append({
            "type": "test",
            "id": test_id,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
        # 更新学习者最后活跃时间
        learner["last_active"] = datetime.datetime.now().isoformat()
        
        # 保存学习者数据
        self.save_learners_data()
        
        # 返回测试题目和测试ID
        return test, test_questions
        
    def submit_test_answers(self, test_id, learner_id, answers, confidence_levels=None):
        """提交测试答案并进行智能评估"""
        if learner_id not in self.learners:
            return False, "学习者不存在"
            
        learner = self.learners[learner_id]
        
        # 查找测试
        test = None
        for history_item in learner["study_history"]:
            if history_item["type"] == "test" and history_item["id"] == test_id:
                # 假设我们在实际应用中会有一个单独的测试存储系统
                # 这里简化处理，重新生成测试题目
                _, test_questions = self.generate_personalized_practice_test(learner_id, num_questions=len(answers))
                break
        
        if not test_questions:
            return False, "测试不存在或已过期"
            
        # 计算得分和评估表现
        correct_count = 0
        total_points = 0
        earned_points = 0
        performance = {}
        knowledge_map = learner.get("knowledge_map", {})
        confidence_map = learner.get("confidence_level", {})
        
        for question_id, user_answer in answers.items():
            # 查找题目
            question = next((q for q in test_questions if q["id"] == question_id), None)
            if not question:
                continue
                
            # 检查答案是否正确（根据题型进行不同的评估）
            is_correct = False
            points = 1.0  # 默认分值
            
            if question["type"] == "single_choice":
                is_correct = user_answer == question.get("correct_answer")
            elif question["type"] == "multiple_choice":
                # 多选题评分（这里使用简单的全对才得分的方式）
                correct_answers = set(question.get("correct_answers", []))
                user_answers = set(user_answer if isinstance(user_answer, list) else [user_answer])
                is_correct = user_answers == correct_answers
            elif question["type"] == "fill_blank":
                # 填空题评分（简单的字符串匹配，实际应用中需要更复杂的文本相似度比较）
                correct_answer = question.get("correct_answer", "")
                is_correct = correct_answer.lower() == user_answer.lower()
            elif question["type"] == "short_answer":
                # 简答题评分（基于关键词匹配，实际应用中可以使用NLP技术进行更复杂的评估）
                key_points = question.get("expected_answer_key_points", [])
                # 简单的关键词匹配
                matched_points = 0
                for point in key_points:
                    if point.lower() in user_answer.lower():
                        matched_points += 1
                is_correct = matched_points >= len(key_points) * 0.7  # 至少匹配70%的关键点
                points = matched_points / len(key_points) if key_points else 1.0
            elif question["type"] == "ordering":
                # 排序题评分
                correct_order = question.get("correct_order", [])
                # 计算Kendall tau相关系数或其他排序相似度指标
                # 这里简化处理，计算完全匹配的位置比例
                matched_positions = sum(1 for i, item in enumerate(user_answer) if i < len(correct_order) and item == correct_order[i])
                points = matched_positions / len(correct_order) if correct_order else 1.0
                is_correct = points >= 0.8  # 至少80%的位置正确
            
            # 更新题目使用次数和正确率
            question["usage_count"] += 1
            # 简单的正确率计算（实际应用中需要更复杂的算法）
            if is_correct:
                correct_count += 1
                earned_points += points
                
            total_points += points
            
            # 更新学习者的知识掌握情况
            subcategory = question.get("subcategory")
            if subcategory not in knowledge_map:
                knowledge_map[subcategory] = 0.0
                
            # 根据答题情况更新掌握程度
            # 结合题目难度和答题情况进行更精细的更新
            difficulty = question.get("difficulty", 1)
            
            if is_correct:
                # 正确回答：难度越高，掌握程度增加越多
                improvement = 0.05 * difficulty
                knowledge_map[subcategory] = min(1.0, knowledge_map[subcategory] + improvement)
            else:
                # 错误回答：难度越低，掌握程度降低越多
                decrement = 0.03 * (6 - difficulty)  # 假设难度范围是1-5
                knowledge_map[subcategory] = max(0.0, knowledge_map[subcategory] - decrement)
                
            # 更新学习者的自信心水平
            if confidence_levels and question_id in confidence_levels:
                confidence = confidence_levels[question_id]
                confidence_map[subcategory] = confidence_map.get(subcategory, []) + [confidence]
                
            # 记录本题的表现
            performance[question_id] = {
                "is_correct": is_correct,
                "user_answer": user_answer,
                "correct_answer": question.get("correct_answer") or question.get("correct_answers") or question.get("expected_answer_key_points"),
                "explanation": question["explanation"],
                "difficulty": difficulty,
                "category": question["category"],
                "subcategory": subcategory,
                "points_earned": earned_points,
                "points_possible": total_points,
                "time_spent_seconds": None  # 在实际应用中，应该记录答题时间
            }
        
        # 计算总得分
        score = (earned_points / total_points) * 100 if total_points > 0 else 0
        
        # 更新学习者数据
        learner["knowledge_map"] = knowledge_map
        learner["confidence_level"] = confidence_map
        learner["last_active"] = datetime.datetime.now().isoformat()
        
        # 保存更新后的数据
        self.save_learners_data()
        self.save_question_bank()
        
        # 生成详细的学习建议
        recommendations = self.generate_detailed_study_recommendations(learner_id)
        
        # 更新学习路径
        self.generate_personalized_learning_path(learner_id)
        
        return True, {
            "score": score,
            "correct_count": correct_count,
            "total_questions": len(answers),
            "points_earned": earned_points,
            "points_possible": total_points,
            "performance": performance,
            "recommendations": recommendations,
            "strengths_weaknesses_analysis": self._analyze_strengths_and_weaknesses(learner_id)
        }
        
    def _analyze_strengths_and_weaknesses(self, learner_id):
        """分析学习者的优势和劣势"""
        if learner_id not in self.learners:
            return {}
            
        learner = self.learners[learner_id]
        knowledge_map = learner.get("knowledge_map", {})
        
        if not knowledge_map:
            return {"analysis": "暂无足够数据进行分析"}
            
        # 按类别分组知识点掌握情况
        category_mastery = defaultdict(list)
        for subcategory, mastery in knowledge_map.items():
            # 查找该子类别的题目，以获取类别信息
            question = next((q for q in self.question_bank if q.get("subcategory") == subcategory), None)
            if question:
                category = question.get("category", "其他")
                category_mastery[category].append((subcategory, mastery))
        
        # 计算每个类别的平均掌握程度
        category_avg_mastery = {}
        for category, subcategories in category_mastery.items():
            avg_mastery = sum(mastery for _, mastery in subcategories) / len(subcategories)
            category_avg_mastery[category] = avg_mastery
        
        # 找出优势和劣势领域
        strengths = []
        weaknesses = []
        
        for category, avg_mastery in category_avg_mastery.items():
            if avg_mastery >= 0.8:
                strengths.append((category, avg_mastery))
            elif avg_mastery < 0.6:
                weaknesses.append((category, avg_mastery))
        
        # 按掌握程度排序
        strengths.sort(key=lambda x: x[1], reverse=True)
        weaknesses.sort(key=lambda x: x[1])
        
        # 生成分析报告
        analysis = {
            "strengths": [
                {"area": category, "mastery_level": mastery} for category, mastery in strengths[:3]
            ],
            "weaknesses": [
                {"area": category, "mastery_level": mastery} for category, mastery in weaknesses[:3]
            ],
            "category_breakdown": category_avg_mastery
        }
        
        return analysis
        
    def generate_detailed_study_recommendations(self, learner_id):
        """生成详细的学习建议"""
        if learner_id not in self.learners:
            return []
            
        learner = self.learners[learner_id]
        
        # 获取学习者的知识掌握情况
        knowledge_map = learner.get("knowledge_map", {})
        learning_behavior = learner.get("learning_behavior", {})
        learning_style = learner.get("learning_style", "balanced")
        
        # 找出掌握程度较低的知识点
        weak_areas = [(subcategory, mastery) for subcategory, mastery in knowledge_map.items() if mastery < 0.6]
        
        # 按掌握程度排序（从低到高）
        weak_areas.sort(key=lambda x: x[1])
        
        # 为每个薄弱知识点生成建议
        recommendations = []
        for subcategory, mastery in weak_areas[:5]:  # 取前5个最薄弱的知识点
            # 查找相关题目
            related_questions = [q for q in self.question_bank if q.get("subcategory") == subcategory]
            
            if related_questions:
                # 根据学习风格调整建议
                learning_resources = []
                
                if learning_style == "visual" or learning_style == "balanced":
                    learning_resources.append("观看相关视频教程")
                    learning_resources.append("查看图表和示意图")
                if learning_style == "auditory" or learning_style == "balanced":
                    learning_resources.append("听相关播客或讲座")
                    learning_resources.append("参与小组讨论")
                if learning_style == "kinesthetic" or learning_style == "balanced":
                    learning_resources.append("进行实践练习")
                    learning_resources.append("完成项目或作业")
                
                # 根据掌握程度确定练习策略
                if mastery < 0.3:
                    practice_strategy = "先理解基础概念，然后逐步进行简单练习"
                    recommended_questions = [q for q in related_questions if q.get("difficulty", 1) <= 2]
                elif mastery < 0.5:
                    practice_strategy = "加强中等难度题目的练习，巩固知识点"
                    recommended_questions = [q for q in related_questions if 2 <= q.get("difficulty", 1) <= 3]
                else:
                    practice_strategy = "挑战较难题目，深化理解"
                    recommended_questions = [q for q in related_questions if q.get("difficulty", 1) >= 3]
                
                # 选择推荐题目
                if recommended_questions:
                    practice_questions = random.sample(recommended_questions, min(5, len(recommended_questions)))
                else:
                    practice_questions = random.sample(related_questions, min(5, len(related_questions)))
                
                recommendations.append({
                    "area": subcategory,
                    "mastery_level": mastery,
                    "recommendation": f"加强对{subcategory}的学习",
                    "learning_resources": learning_resources,
                    "practice_strategy": practice_strategy,
                    "practice_questions": [q["id"] for q in practice_questions],
                    "estimated_time_hours": max(1.0, (1 - mastery) * 3)  # 掌握程度越低，建议学习时间越长
                })
        
        # 如果没有薄弱知识点，生成总体复习建议
        if not recommendations:
            recommendations.append({
                "area": "总体复习",
                "mastery_level": 1.0,
                "recommendation": "继续保持良好的学习状态，可以挑战更难的题目或扩展相关知识点的学习",
                "learning_resources": ["参考进阶教材", "参与竞赛或项目", "教授他人以巩固知识"],
                "practice_strategy": "进行综合练习和模拟考试",
                "practice_questions": [],
                "estimated_time_hours": 2.0
            })
            
        return recommendations
        
    def generate_personalized_learning_path(self, learner_id):
        """生成个性化学习路径"""
        if learner_id not in self.learners:
            return None, "学习者不存在"
            
        learner = self.learners[learner_id]
        
        # 获取学习者的目标、学科和知识掌握情况
        goals = learner.get("goals", [])
        subjects = learner.get("subjects", [])
        knowledge_map = learner.get("knowledge_map", {})
        prior_knowledge = learner.get("prior_knowledge", {})
        learning_style = learner.get("learning_style", "balanced")
        
        # 生成学习路径
        learning_path = {
            "id": f"advanced_path_{learner_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            "learner_id": learner_id,
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
            "goals": goals,
            "subjects": subjects,
            "learning_style": learning_style,
            "estimated_total_time_hours": 0,
            "completed_time_hours": 0,
            "progress": 0.0,
            "milestones": [],
            "modules": []
        }
        
        # 按类别分组题目
        questions_by_category = defaultdict(list)
        for question in self.question_bank:
            category = question.get("category")
            questions_by_category[category].append(question)
            
        # 计算每个类别的重要性权重
        category_weights = {}
        for category in questions_by_category.keys():
            # 基础权重
            weight = 1.0
            
            # 如果是学习者指定的学科，增加权重
            if subjects and category in subjects:
                weight *= 1.5
                
            # 如果与学习者的目标相关，增加权重
            if goals:
                # 简单的关键词匹配，实际应用中可以使用NLP进行更复杂的匹配
                for goal in goals:
                    if category.lower() in goal.lower():
                        weight *= 1.3
                        break
                        
            category_weights[category] = weight
            
        # 为每个类别生成学习模块
        total_estimated_time = 0
        
        for category, questions in questions_by_category.items():
            # 如果学习者指定了学科，只包含指定学科的内容
            if subjects and category not in subjects:
                continue
                
            # 找出该类别下的所有子类别
            subcategories = set(q.get("subcategory") for q in questions)
            
            # 计算每个子类别的掌握程度和重要性
            subcategory_info = []
            
            for subcat in subcategories:
                # 获取掌握程度
                mastery = knowledge_map.get(subcat, 0.5)  # 默认掌握程度为0.5
                
                # 获取该子类别的题目难度分布
                subcat_questions = [q for q in questions if q.get("subcategory") == subcat]
                
                if subcat_questions:
                    # 计算平均难度
                    avg_difficulty = sum(q.get("difficulty", 1) for q in subcat_questions) / len(subcat_questions)
                    
                    # 计算该子类别的题目数量
                    num_questions = len(subcat_questions)
                    
                    # 计算预计学习时间
                    estimated_time = num_questions * 0.1 * (1 + (1 - mastery))  # 掌握程度越低，预计学习时间越长
                    
                    # 计算优先级分数（综合考虑掌握程度、权重和难度）
                    priority_score = (1 - mastery) * category_weights[category] * avg_difficulty
                    
                    subcategory_info.append({
                        "subcategory": subcat,
                        "mastery": mastery,
                        "priority_score": priority_score,
                        "estimated_time": estimated_time,
                        "num_questions": num_questions,
                        "avg_difficulty": avg_difficulty
                    })
            
            # 按优先级排序子类别
            subcategory_info.sort(key=lambda x: x["priority_score"], reverse=True)
            
            # 为该类别创建学习模块
            module_estimated_time = sum(info["estimated_time"] for info in subcategory_info)
            total_estimated_time += module_estimated_time
            
            module = {
                "category": category,
                "priority": 1 if category in subjects else 2,  # 指定学科优先级更高
                "estimated_time_hours": module_estimated_time,
                "completed_time_hours": 0,
                "progress": 0.0,
                "submodules": []
            }
            
            # 为每个子类别创建子模块
            for info in subcategory_info:
                subcat = info["subcategory"]
                
                # 找出该子类别的题目
                subcat_questions = [q for q in questions if q.get("subcategory") == subcat]
                
                if subcat_questions:
                    # 根据掌握程度和难度确定练习题目
                    if info["mastery"] < 0.3:
                        # 基础阶段：以简单题目为主
                        practice_questions = [q for q in subcat_questions if q.get("difficulty", 1) <= 2]
                    elif info["mastery"] < 0.6:
                        # 提高阶段：以中等难度题目为主
                        practice_questions = [q for q in subcat_questions if 2 <= q.get("difficulty", 1) <= 3]
                    else:
                        # 巩固阶段：以较难题目为主
                        practice_questions = [q for q in subcat_questions if q.get("difficulty", 1) >= 3]
                    
                    # 如果没有足够的题目，补充其他难度的题目
                    if len(practice_questions) < 3:
                        practice_questions = subcat_questions[:5]  # 最多取5道题
                    
                    # 随机选择一些题目
                    selected_questions = random.sample(practice_questions, min(5, len(practice_questions)))
                    
                    # 根据学习风格调整学习活动建议
                    learning_activities = []
                    
                    if learning_style == "visual" or learning_style == "balanced":
                        learning_activities.append("创建概念图或思维导图")
                        learning_activities.append("观看相关可视化教程")
                    if learning_style == "auditory" or learning_style == "balanced":
                        learning_activities.append("听相关讲座或播客")
                        learning_activities.append("解释概念给他人听")
                    if learning_style == "kinesthetic" or learning_style == "balanced":
                        learning_activities.append("进行实践练习")
                        learning_activities.append("完成相关项目或作业")
                    
                    submodule = {
                        "subcategory": subcat,
                        "mastery_level": info["mastery"],
                        "priority_score": info["priority_score"],
                        "estimated_time_hours": info["estimated_time"],
                        "progress": 0.0,
                        "practice_questions": [q["id"] for q in selected_questions],
                        "learning_activities": learning_activities,
                        "resources": [],  # 在实际应用中，这里可以推荐具体的学习资源
                        "assessment_criteria": ["掌握基础概念", "能够解决典型问题", "能够应用到实际场景"]
                    }
                    
                    module["submodules"].append(submodule)
                    
            # 添加模块到学习路径
            learning_path["modules"].append(module)
            
        # 按优先级排序模块
        learning_path["modules"].sort(key=lambda x: (x["priority"], -x["estimated_time_hours"]))
        
        # 设置总预计时间
        learning_path["estimated_total_time_hours"] = total_estimated_time
        
        # 创建里程碑
        if goals:
            for i, goal in enumerate(goals):
                learning_path["milestones"].append({
                    "id": f"milestone_{i+1}",
                    "name": goal,
                    "description": f"完成{goal}的学习目标",
                    "estimated_time_hours": total_estimated_time / len(goals) * (i+1),
                    "completed": False,
                    "deadline": None  # 在实际应用中，可以设置截止日期
                })
        
        # 更新学习者的学习路径
        self.learning_paths[learner_id] = learning_path
        
        # 保存学习路径
        self.save_learning_paths()
        
        return learning_path
        
    def get_detailed_learner_progress(self, learner_id):
        """获取学习者详细进度"""
        if learner_id not in self.learners:
            return None, "学习者不存在"
            
        learner = self.learners[learner_id]
        
        # 计算总体进度
        total_questions = len(self.question_bank)
        attempted_questions = len(learner.get("performance", {}))
        progress_percentage = (attempted_questions / total_questions) * 100 if total_questions > 0 else 0
        
        # 计算知识点掌握情况统计
        knowledge_map = learner.get("knowledge_map", {})
        
        if knowledge_map:
            avg_mastery = sum(knowledge_map.values()) / len(knowledge_map)
            strong_areas = [subcat for subcat, mastery in knowledge_map.items() if mastery >= 0.8]
            weak_areas = [subcat for subcat, mastery in knowledge_map.items() if mastery < 0.5]
            
            # 计算进步趋势（简单的线性趋势，实际应用中可以使用更复杂的时间序列分析）
            # 这里简化处理，假设最近的表现比早期的好
            improvement_trend = "positive" if avg_mastery > 0.6 else "neutral" if avg_mastery > 0.4 else "negative"
        else:
            avg_mastery = 0.0
            strong_areas = []
            weak_areas = []
            improvement_trend = "neutral"
            
        # 获取最近的测试成绩
        recent_tests = [item for item in learner.get("study_history", []) if item["type"] == "test"][-5:]
        recent_scores = []
        
        # 计算学习活跃度和学习行为分析
        study_history = learner.get("study_history", [])
        learning_behavior = {
            "total_study_sessions": len(study_history),
            "recent_activity": "活跃" if len(study_history) > 5 else "一般" if len(study_history) > 0 else "不活跃",
            "preferred_times": {},  # 在实际应用中，可以分析学习时间偏好
            "preferred_subjects": {}  # 在实际应用中，可以分析偏好的学科
        }
        
        # 计算学习效率指标
        if study_history:
            # 简单的效率计算，实际应用中需要更复杂的算法
            learning_efficiency = avg_mastery / len(study_history) * 100 if len(study_history) > 0 else 0
        else:
            learning_efficiency = 0
            
        # 获取学习路径信息
        learning_path = self.learning_paths.get(learner_id, {})
        
        # 生成进度报告
        progress_report = {
            "learner_id": learner_id,
            "name": learner.get("name"),
            "overall_progress": progress_percentage,
            "avg_mastery_level": avg_mastery,
            "strong_areas": strong_areas,
            "weak_areas": weak_areas,
            "improvement_trend": improvement_trend,
            "learning_behavior": learning_behavior,
            "learning_efficiency": learning_efficiency,
            "recent_test_count": len(recent_tests),
            "learning_path": learning_path,
            "last_active": learner.get("last_active"),
            "next_recommended_actions": self._get_next_recommended_actions(learner_id)
        }
        
        return progress_report
        
    def _get_next_recommended_actions(self, learner_id):
        """获取下一步推荐操作"""
        if learner_id not in self.learners:
            return []
            
        # 获取学习者进度
        progress = self.get_detailed_learner_progress(learner_id)
        if isinstance(progress, tuple):
            progress = progress[0]  # 处理错误情况
            
        if not progress:
            return []
            
        recommended_actions = []
        
        # 根据总体进度推荐操作
        if progress["overall_progress"] < 30:
            recommended_actions.append("继续完成基础内容的学习")
        elif progress["overall_progress"] < 70:
            recommended_actions.append("加强薄弱环节的练习")
        else:
            recommended_actions.append("进行综合复习和模拟考试")
            
        # 根据掌握程度推荐操作
        if progress["avg_mastery_level"] < 0.5:
            recommended_actions.append("重新学习基础概念")
        elif progress["avg_mastery_level"] < 0.8:
            recommended_actions.append("进行进阶练习和应用")
        else:
            recommended_actions.append("探索相关扩展内容")
            
        # 根据进步趋势推荐操作
        if progress["improvement_trend"] == "negative":
            recommended_actions.append("调整学习方法，寻求帮助")
        elif progress["improvement_trend"] == "neutral":
            recommended_actions.append("尝试新的学习策略")
            
        # 根据学习活跃度推荐操作
        if progress["learning_behavior"].get("recent_activity") == "不活跃":
            recommended_actions.append("制定学习计划，保持规律学习")
            
        return recommended_actions
        
    def search_and_recommend_resources(self, query, learner_id=None):
        """搜索并推荐学习资源"""
        # 在实际应用中，这里会连接到外部资源库或API
        # 这里简化处理，返回示例资源
        
        example_resources = [
            {
                "title": "Python官方教程",
                "type": "教程",
                "url": "https://docs.python.org/3/tutorial/",
                "description": "Python官方提供的入门教程，涵盖基础语法和核心概念",
                "difficulty": "初级",
                "duration": "10小时"
            },
            {
                "title": "机器学习实战",
                "type": "书籍",
                "url": "https://example.com/ml-book",
                "description": "通过实例讲解机器学习算法和应用",
                "difficulty": "中级",
                "duration": "30小时"
            },
            {
                "title": "深度学习入门课程",
                "type": "在线课程",
                "url": "https://example.com/deep-learning",
                "description": "介绍深度学习的基本概念和应用",
                "difficulty": "中级",
                "duration": "20小时"
            },
            {
                "title": "数据科学项目实践",
                "type": "项目教程",
                "url": "https://example.com/data-science-projects",
                "description": "通过实际项目学习数据科学技能",
                "difficulty": "高级",
                "duration": "40小时"
            }
        ]
        
        # 如果提供了学习者ID，可以根据学习者的情况进行个性化推荐
        if learner_id and learner_id in self.learners:
            learner = self.learners[learner_id]
            learning_style = learner.get("learning_style", "balanced")
            knowledge_map = learner.get("knowledge_map", {})
            
            # 简单的个性化筛选，实际应用中可以使用更复杂的推荐算法
            filtered_resources = []
            
            for resource in example_resources:
                # 根据学习风格进行筛选
                if learning_style == "visual" and resource["type"] in ["教程", "在线课程"]:
                    filtered_resources.append(resource)
                elif learning_style == "auditory" and resource["type"] in ["在线课程"]:
                    filtered_resources.append(resource)
                elif learning_style == "kinesthetic" and resource["type"] in ["项目教程"]:
                    filtered_resources.append(resource)
                elif learning_style == "balanced":
                    filtered_resources.append(resource)
                
            return filtered_resources[:3]  # 最多返回3个资源
        
        # 没有提供学习者ID，返回所有资源
        return example_resources
        
    def predict_exam_performance(self, learner_id, exam_type):
        """预测考试表现"""
        if learner_id not in self.learners:
            return None, "学习者不存在"
            
        learner = self.learners[learner_id]
        knowledge_map = learner.get("knowledge_map", {})
        
        # 简化的预测模型，实际应用中可以使用更复杂的机器学习模型
        
        # 计算平均掌握程度
        if knowledge_map:
            avg_mastery = sum(knowledge_map.values()) / len(knowledge_map)
        else:
            avg_mastery = 0.5  # 默认掌握程度为中等
            
        # 根据考试类型调整预测
        exam_adjustment = {
            "basic": 0.1,  # 基础考试调整因子
            "intermediate": 0.0,  # 中级考试调整因子
            "advanced": -0.1  # 高级考试调整因子
        }.get(exam_type, 0.0)
        
        # 计算预测分数（0-100）
        predicted_score = max(0, min(100, (avg_mastery + exam_adjustment) * 100))
        
        # 生成通过概率（基于预测分数和假设的及格分数）
        passing_score = 60  # 假设及格分数为60分
        
        if predicted_score >= passing_score + 10:
            passing_probability = "高（>80%）"
        elif predicted_score >= passing_score:
            passing_probability = "中等（60-80%）"
        elif predicted_score >= passing_score - 10:
            passing_probability = "低（40-60%）"
        else:
            passing_probability = "很低（<40%）"
        
        # 生成详细的预测报告
        prediction_report = {
            "exam_type": exam_type,
            "predicted_score": predicted_score,
            "passing_probability": passing_probability,
            "recommendations": [],
            "confidence_level": "中等"  # 在实际应用中，可以根据数据量和模型性能调整
        }
        
        # 根据预测结果生成建议
        if predicted_score < passing_score:
            prediction_report["recommendations"].append("需要加强复习，特别是薄弱环节")
            prediction_report["recommendations"].append("增加模拟考试练习")
        elif predicted_score < 80:
            prediction_report["recommendations"].append("继续保持，重点巩固薄弱知识点")
        else:
            prediction_report["recommendations"].append("保持良好状态，考试前进行适当复习")
            
        return prediction_report
        
    def generate_ai_assistant_response(self, learner_id, query):
        """生成AI助手回答"""
        if not self.qa_pipeline:
            return "AI助手功能不可用，请稍后再试。"
            
        # 在实际应用中，这里会使用更复杂的问答系统
        # 这里简化处理，使用预训练模型生成回答
        
        try:
            # 构建上下文（基于学习者的知识图谱和学习历史）
            if learner_id and learner_id in self.learners:
                learner = self.learners[learner_id]
                knowledge_map = learner.get("knowledge_map", {})
                
                # 构建简单的上下文
                context = "学习者的知识掌握情况：\n"
                for subcategory, mastery in sorted(knowledge_map.items(), key=lambda x: x[1])[:3]:
                    context += f"- {subcategory}：{mastery:.2f}\n"
            else:
                context = "这是一个关于AI考试准备的问答系统。"
                
            # 使用QA模型生成回答
            result = self.qa_pipeline(question=query, context=context)
            
            return result["answer"]
        except Exception as e:
            print(f"生成AI助手回答失败：{e}")
            # 回退到简单回答
            return f"关于'{query}'的问题，我建议你查阅相关学习资料或咨询老师。"

# 使用示例
if __name__ == "__main__":
    # 创建高级AI考试准备系统实例
    advanced_exam_prep_system = AdvancedAIExamPrepSystem()
    
    # 添加高级学习者
    print("添加高级学习者示例：")
    advanced_learner = advanced_exam_prep_system.add_learner(
        learner_id="advanced_learner001",
        name="李四",
        email="lisi@example.com",
        goals=["通过机器学习工程师认证", "掌握深度学习算法"],
        subjects=["机器学习", "深度学习"],
        prior_knowledge={"Python编程": 0.8, "数学基础": 0.7},
        learning_style="visual"
    )
    print(f"已添加高级学习者：{advanced_learner['name']} (ID: {advanced_learner['id']})")
    print(f"学习风格：{advanced_learner['learning_style']}")
    
    # 生成个性化练习测试
    print("\n生成个性化练习测试示例：")
    test_info, test_questions = advanced_exam_prep_system.generate_personalized_practice_test(
        "advanced_learner001", 
        category="机器学习", 
        num_questions=2,
        adaptive=True
    )
    print(f"已生成个性化测试，ID: {test_info['id']}")
    print(f"预计完成时间：{test_info['estimated_time_minutes']:.1f}分钟")
    print(f"测试包含{len(test_questions)}道题目：")
    for i, question in enumerate(test_questions, 1):
        print(f"{i}. {question['content']}")
        if question.get("options"):
            print(f"   选项: {', '.join(question['options'])}")
        print(f"   题型: {question['type']}")
        print(f"   难度: {question['difficulty']}")
    
    # 模拟提交答案和自信心水平
    print("\n提交测试答案和自信心水平示例：")
    # 这里我们假设用户回答了部分题目正确，部分错误
    answers = {}
    confidence_levels = {}
    
    for question in test_questions:
        if question["type"] == "single_choice":
            # 随机决定是否正确回答
            is_correct = random.choice([True, False])
            if is_correct:
                answers[question["id"]] = question["correct_answer"]
            else:
                # 选择一个错误的选项
                wrong_options = [opt for opt in question["options"] if opt != question["correct_answer"]]
                answers[question["id"]] = random.choice(wrong_options) if wrong_options else question["options"][0]
            
            # 设置自信心水平（1-5）
            confidence_levels[question["id"]] = random.randint(3, 5) if is_correct else random.randint(1, 3)
        elif question["type"] == "fill_blank":
            # 随机决定是否正确回答
            is_correct = random.choice([True, False])
            answers[question["id"]] = question["correct_answer"] if is_correct else "错误答案"
            
            # 设置自信心水平（1-5）
            confidence_levels[question["id"]] = random.randint(3, 5) if is_correct else random.randint(1, 3)
    
    success, result = advanced_exam_prep_system.submit_test_answers(
        test_info['id'], 
        "advanced_learner001", 
        answers,
        confidence_levels
    )
    
    print(f"提交结果：{success}")
    print(f"测试得分：{result['score']:.2f}分")
    print(f"获得分数：{result['points_earned']:.2f}/{result['points_possible']:.2f}")
    
    # 查看详细的学习建议
    print("\n详细学习建议示例：")
    recommendations = result.get("recommendations", [])
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['recommendation']} (掌握程度: {rec['mastery_level']:.2f})")
        print(f"   预计学习时间: {rec['estimated_time_hours']:.1f}小时")
        print(f"   学习资源建议: {', '.join(rec['learning_resources'])}")
        print(f"   练习策略: {rec['practice_strategy']}")
    
    # 查看优势劣势分析
    print("\n优势劣势分析示例：")
    analysis = result.get("strengths_weaknesses_analysis", {})
    print(f"优势领域：")
    for strength in analysis.get("strengths", []):
        print(f"- {strength['area']}: 掌握程度 {strength['mastery_level']:.2f}")
    print(f"劣势领域：")
    for weakness in analysis.get("weaknesses", []):
        print(f"- {weakness['area']}: 掌握程度 {weakness['mastery_level']:.2f}")
    
    # 获取详细学习者进度
    print("\n详细学习者进度示例：")
    progress = advanced_exam_prep_system.get_detailed_learner_progress("advanced_learner001")
    print(f"学习者：{progress['name']}")
    print(f"总体进度：{progress['overall_progress']:.2f}%")
    print(f"平均掌握程度：{progress['avg_mastery_level']:.2f}")
    print(f"进步趋势：{progress['improvement_trend']}")
    print(f"学习效率：{progress['learning_efficiency']:.2f}")
    print(f"下一步推荐操作：")
    for action in progress.get("next_recommended_actions", []):
        print(f"- {action}")
    
    # 搜索并推荐学习资源
    print("\n搜索并推荐学习资源示例：")
    resources = advanced_exam_prep_system.search_and_recommend_resources("机器学习", "advanced_learner001")
    print(f"为您推荐{len(resources)}个学习资源：")
    for i, resource in enumerate(resources, 1):
        print(f"{i}. {resource['title']} ({resource['type']})")
        print(f"   描述: {resource['description']}")
        print(f"   难度: {resource['difficulty']}")
        print(f"   预计学习时间: {resource['duration']}")
    
    # 预测考试表现
    print("\n预测考试表现示例：")
    prediction = advanced_exam_prep_system.predict_exam_performance("advanced_learner001", "intermediate")
    print(f"考试类型：{prediction['exam_type']}")
    print(f"预测分数：{prediction['predicted_score']:.2f}")
    print(f"通过概率：{prediction['passing_probability']}")
    print(f"备考建议：")
    for rec in prediction.get("recommendations", []):
        print(f"- {rec}")
    
    # 生成AI助手回答
    print("\nAI助手回答示例：")
    query = "什么是机器学习中的聚类算法？"
    assistant_response = advanced_exam_prep_system.generate_ai_assistant_response("advanced_learner001", query)
    print(f"问题: {query}")
    print(f"回答: {assistant_response}")
    
    # 添加高级题目（简答题）
    print("\n添加高级题目（简答题）示例：")
    new_question = advanced_exam_prep_system.add_question(
        content="请解释什么是监督学习，并举例说明其应用场景。",
        question_type="short_answer",
        correct_answer=None,  # 简答题没有固定的正确答案，而是有预期的关键点
        explanation="监督学习是一种机器学习方法，模型通过学习带有标签的训练数据来预测新数据的标签。常见的监督学习算法包括线性回归、决策树、随机森林和神经网络等。应用场景包括图像分类、语音识别、自然语言处理、推荐系统等。",
        category="机器学习",
        subcategory="算法类型",
        difficulty=3,
        expected_answer_key_points=[
            "使用带有标签的训练数据",
            "学习输入到输出的映射关系",
            "能够预测新数据的标签",
            "包括分类和回归任务",
            "应用场景如：图像识别、语音识别、预测分析等"
        ],
        tags=["机器学习", "监督学习", "算法类型"],
        estimated_time_seconds=180,
        keywords=["监督学习", "标签数据", "预测", "分类", "回归"]
    )
    print(f"已添加高级题目：{new_question['content']} (ID: {new_question['id']})")
    print(f"题型: {new_question['type']}")
    print(f"预计答题时间: {new_question['estimated_time_seconds']}秒")
    
    # 查看更新后的题库
    print(f"\n更新后的高级题库数量：{len(advanced_exam_prep_system.question_bank)}道题目")
```

## 最佳实践

### 1. 如何选择合适的AI考试准备工具

在选择AI考试准备工具时，应考虑以下几个关键因素：

- **考试类型和内容匹配度**：确保工具覆盖了您需要准备的考试内容和题型
- **个性化学习能力**：选择能够根据您的水平和进度提供个性化学习路径的工具
- **交互体验**：良好的用户界面和交互体验能够提高学习效率
- **数据分析能力**：工具应能够提供详细的学习数据和分析，帮助您了解自己的优势和不足
- **资源丰富度**：除了题目外，是否提供了视频、教程等多种学习资源
- **成本效益**：评估工具的价格是否合理，是否提供免费试用
- **用户评价**：参考其他用户的评价和反馈
- **技术支持**：是否提供良好的技术支持和更新服务

### 2. 如何有效使用AI进行考试准备

为了充分发挥AI考试准备工具的作用，建议遵循以下策略：

- **制定明确的学习目标**：设定具体、可衡量的学习目标，如掌握特定知识点、提高特定题型的正确率等
- **结合AI和传统学习方法**：AI工具可以作为传统学习方法的补充，但不应完全替代传统学习
- **定期使用和跟踪进度**：养成定期使用AI工具的习惯，并定期查看学习进度报告
- **重视薄弱环节**：根据AI工具的分析结果，重点加强薄弱环节的学习
- **积极参与互动练习**：不仅仅是被动学习，还要积极参与AI提供的互动练习和模拟考试
- **合理安排学习时间**：根据AI工具的建议，合理安排每天的学习时间，避免疲劳学习
- **利用AI生成的个性化建议**：认真阅读并执行AI工具生成的个性化学习建议
- **保持学习动力**：设置小目标，通过AI工具的反馈和奖励机制保持学习动力

### 3. AI考试准备的常见误区

在使用AI进行考试准备时，应避免以下常见误区：

- **过度依赖AI**：AI是辅助工具，不能替代您的主动学习和思考
- **忽视基础知识**：不要因为AI能够提供快速答案而忽视对基础知识的理解
- **只关注得分而不关注学习过程**：重要的是真正掌握知识，而不仅仅是提高分数
- **忽视错题分析**：不仅仅要知道答案是否正确，更要理解为什么正确，为什么错误
- **学习时间过长而效率低下**：学习效果并不完全取决于时间长短，更重要的是学习质量
- **忽视模拟考试的重要性**：模拟考试不仅可以评估学习效果，还可以帮助您熟悉考试环境和节奏
- **不根据自身情况调整学习计划**：AI提供的建议是基于数据分析的，但您也应该根据自己的实际情况进行调整
- **忽视身体和心理健康**：保持良好的身体和心理状态对于考试准备同样重要

### 4. AI考试准备的伦理和法律问题

在使用AI进行考试准备时，需要注意以下伦理和法律问题：

- **学术诚信**：使用AI进行学习是可以的，但在实际考试中使用AI属于作弊行为
- **数据隐私**：了解AI工具如何收集、存储和使用您的个人数据
- **版权问题**：确保您使用的AI工具和学习材料符合版权法规
- **公平性**：注意AI可能存在的偏见，避免过度依赖单一来源的信息
- **透明度**：了解AI工具的工作原理，特别是它如何生成学习建议和评估结果
- **负责任使用**：负责任地使用AI工具，不要用于不当目的
- **遵守考试规则**：了解并遵守您将参加的考试的规则和规定
- **平衡技术与人文**：记住教育的本质是人的发展，技术只是辅助手段

通过遵循这些最佳实践，您可以更有效地使用AI进行考试准备，提高学习效率和考试成绩。同时，也要注意保持平衡，不要让技术完全主导您的学习过程。