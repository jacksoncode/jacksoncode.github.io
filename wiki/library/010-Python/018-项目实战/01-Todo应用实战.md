# Python 项目实战：Todo 应用

## 1. 项目概述

我们将使用 Python + Flask 构建一个完整的 Todo 待办事项应用，包含：

- 用户认证（注册/登录）
- Todo CRUD 操作
- 数据持久化（SQLite）
- RESTful API
- 单元测试

## 2. 项目结构

```
todo-app/
├── app.py              # 主应用入口
├── config.py           # 配置文件
├── models.py           # 数据模型
├── routes.py           # 路由定义
├── auth.py             # 认证逻辑
├── requirements.txt    # 依赖
├── tests/              # 测试目录
│   ├── __init__.py
│   ├── conftest.py
│   └── test_api.py
└── instance/          # 数据库目录
    └── todo.db
```

## 3. 核心代码实现

### 配置

```python
# config.py
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///todo.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
```

### 数据模型

```python
# models.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    todos = db.relationship('Todo', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Todo(db.Model):
    __tablename__ = 'todos'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.Integer, default=1)  # 1-5
    due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'priority': self.priority,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
```

### 认证逻辑

```python
# auth.py
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app

def generate_token(user_id):
    """生成 JWT token"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES'],
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

def decode_token(token):
    """解码 JWT token"""
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """认证装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        user_id = decode_token(token)
        if not user_id:
            return jsonify({'error': 'Token is invalid'}), 401
        
        return f(user_id, *args, **kwargs)
    
    return decorated
```

### 路由定义

```python
# routes.py
from flask import Blueprint, request, jsonify
from models import db, User, Todo
from auth import generate_token, token_required

api = Blueprint('api', __name__)

# 用户注册
@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing username or password'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(username=data['username'], email=data.get('email', ''))
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

# 用户登录
@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    user = User.query.filter_by(username=data.get('username')).first()
    
    if not user or not user.check_password(data.get('password', '')):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    token = generate_token(user.id)
    
    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'username': user.username
        }
    }), 200

# 获取所有 Todo
@api.route('/todos', methods=['GET'])
@token_required
def get_todos(user_id):
    completed = request.args.get('completed', type=lambda x: x.lower() == 'true')
    
    query = Todo.query.filter_by(user_id=user_id)
    
    if completed is not None:
        query = query.filter_by(completed=completed)
    
    todos = query.order_by(Todo.priority.desc(), Todo.created_at.desc()).all()
    
    return jsonify({
        'todos': [todo.to_dict() for todo in todos],
        'total': len(todos)
    }), 200

# 创建 Todo
@api.route('/todos', methods=['POST'])
@token_required
def create_todo(user_id):
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    
    todo = Todo(
        title=data['title'],
        description=data.get('description'),
        priority=data.get('priority', 1),
        due_date=data.get('due_date'),
        user_id=user_id
    )
    
    db.session.add(todo)
    db.session.commit()
    
    return jsonify(todo.to_dict()), 201

# 更新 Todo
@api.route('/todos/<int:todo_id>', methods=['PUT'])
@token_required
def update_todo(user_id, todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
    
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    
    data = request.get_json()
    
    if 'title' in data:
        todo.title = data['title']
    if 'description' in data:
        todo.description = data['description']
    if 'completed' in data:
        todo.completed = data['completed']
    if 'priority' in data:
        todo.priority = data['priority']
    if 'due_date' in data:
        todo.due_date = data['due_date']
    
    db.session.commit()
    
    return jsonify(todo.to_dict()), 200

# 删除 Todo
@api.route('/todos/<int:todo_id>', methods=['DELETE'])
@token_required
def delete_todo(user_id, todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
    
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    
    db.session.delete(todo)
    db.session.commit()
    
    return jsonify({'message': 'Todo deleted'}), 200
```

### 主应用

```python
# app.py
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models import db
from routes import api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    
    app.register_blueprint(api, url_prefix='/api')
    
    @app.route('/')
    def index():
        return jsonify({'message': 'Todo API', 'version': '1.0'})
    
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy'}), 200
    
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
```

## 4. 依赖文件

```
# requirements.txt
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-CORS==4.0.0
PyJWT==2.8.0
Werkzeug==3.0.1
pytest==7.4.3
pytest-flask==1.3.0
```

## 5. 测试代码

```python
# tests/conftest.py
import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    # 注册并登录获取 token
    client.post('/api/register', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    
    response = client.post('/api/login', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    
    token = response.get_json()['token']
    return {'Authorization': f'Bearer {token}'}
```

```python
# tests/test_api.py
def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'healthy'

def test_register(client):
    response = client.post('/api/register', json={
        'username': 'newuser',
        'password': 'newpass'
    })
    assert response.status_code == 201

def test_login(client):
    # 先注册
    client.post('/api/register', json={
        'username': 'user1',
        'password': 'pass1'
    })
    
    # 再登录
    response = client.post('/api/login', json={
        'username': 'user1',
        'password': 'pass1'
    })
    assert response.status_code == 200
    assert 'token' in response.get_json()

def test_create_todo(client, auth_headers):
    response = client.post('/api/todos', 
        json={'title': 'Test Todo'},
        headers=auth_headers
    )
    assert response.status_code == 201
    assert response.get_json()['title'] == 'Test Todo'

def test_get_todos(client, auth_headers):
    # 创建一些 todos
    client.post('/api/todos', 
        json={'title': 'Todo 1'},
        headers=auth_headers
    )
    client.post('/api/todos',
        json={'title': 'Todo 2'},
        headers=auth_headers
    )
    
    response = client.get('/api/todos', headers=auth_headers)
    assert response.status_code == 200
    assert response.get_json()['total'] == 2

def test_update_todo(client, auth_headers):
    # 创建 todo
    create_resp = client.post('/api/todos',
        json={'title': 'Original'},
        headers=auth_headers
    )
    todo_id = create_resp.get_json()['id']
    
    # 更新
    response = client.put(f'/api/todos/{todo_id}',
        json={'title': 'Updated', 'completed': True},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.get_json()['title'] == 'Updated'
    assert response.get_json()['completed'] is True

def test_delete_todo(client, auth_headers):
    # 创建 todo
    create_resp = client.post('/api/todos',
        json={'title': 'To Delete'},
        headers=auth_headers
    )
    todo_id = create_resp.get_json()['id']
    
    # 删除
    response = client.delete(f'/api/todos/{todo_id}', headers=auth_headers)
    assert response.status_code == 200
    
    # 确认删除
    get_resp = client.get('/api/todos', headers=auth_headers)
    assert get_resp.get_json()['total'] == 0
```

## 6. 运行项目

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python app.py

# 运行测试
pytest tests/ -v

# API 测试
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "123456"}'
```

## 7. 进阶功能建议

1. **任务分类**：添加分类/标签功能
2. **提醒通知**：集成邮件或 WebSocket 推送
3. **搜索功能**：全文搜索 Todo
4. **数据导出**：导出为 JSON/CSV
5. **协作功能**：分享 Todo 列表给其他用户
6. **统计图表**：看板视图、完成率统计
