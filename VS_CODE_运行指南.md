# 图书管理系统 - VS Code 运行指南

## 🚀 快速开始

### 1. 打开项目
- 在VS Code中打开项目文件夹：`C:\school\pbl5\management_project\library_management_project`

### 2. 安装Python扩展
确保VS Code已安装以下扩展：
- Python (Microsoft)
- Pylance

### 3. 设置Python解释器
1. 按 `Ctrl+Shift+P` 打开命令面板
2. 输入 "Python: Select Interpreter"
3. 选择您的Python 3.13解释器

### 4. 安装依赖包
在VS Code终端中运行：
```bash
pip install flask flask-sqlalchemy flask-login flask-wtf flask-bcrypt wtforms pymysql python-dotenv
```

### 5. 配置数据库（选择一种方式）

#### 方式A：使用MySQL（推荐）
1. 确保MySQL服务正在运行
2. 在MySQL中创建数据库：
   ```sql
   CREATE DATABASE library_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. 检查 `config.py` 中的数据库连接配置：
   ```python
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:你的密码@localhost/library_management'
   ```

#### 方式B：使用SQLite（简单）
修改 `config.py`：
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///library.db'  # 改为SQLite
```

### 6. 运行方式

#### 方式1：使用VS Code调试器
1. 按 `F5` 或点击调试面板的运行按钮
2. 选择 "Python: Flask" 配置
3. 系统会自动启动Flask应用

#### 方式2：使用VS Code任务
1. 按 `Ctrl+Shift+P`
2. 输入 "Tasks: Run Task"
3. 选择 "完整启动流程"

#### 方式3：手动运行
在VS Code终端中运行：
```bash
# 初始化数据库
python create_database.py

# 启动应用
python run.py
```

#### 方式4：简化启动
```bash
python simple_start.py
```

## 🔧 VS Code 配置文件

### .vscode/launch.json
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/run.py",
            "console": "integratedTerminal",
            "justMyCode": true,
            "env": {
                "FLASK_ENV": "development",
                "FLASK_DEBUG": "1"
            }
        },
        {
            "name": "Python: 初始化数据库",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/create_database.py",
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}
```

### .vscode/tasks.json
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "安装依赖包",
            "type": "shell",
            "command": "pip",
            "args": ["install", "-r", "requirements.txt"],
            "group": "build"
        },
        {
            "label": "创建数据库",
            "type": "shell",
            "command": "python",
            "args": ["create_database.py"],
            "group": "build"
        },
        {
            "label": "启动Flask应用",
            "type": "shell",
            "command": "python",
            "args": ["run.py"],
            "group": "build"
        },
        {
            "label": "完整启动流程",
            "dependsOrder": "sequence",
            "dependsOn": ["安装依赖包", "创建数据库", "启动Flask应用"],
            "group": {"kind": "build", "isDefault": true}
        }
    ]
}
```

## 📋 访问信息

启动成功后：
- **访问地址**: http://localhost:5000
- **默认管理员**: admin / admin123
- **测试用户**: testuser / test123（如果存在）

## 🛠️ 常见问题

### 1. 依赖安装失败
```bash
# 清除pip缓存
pip cache purge

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 2. 数据库连接失败
- 检查MySQL服务是否启动
- 确认数据库用户名和密码
- 或者改用SQLite数据库

### 3. 端口占用
```bash
# 查找占用5000端口的进程
netstat -ano | findstr :5000

# 终止进程
taskkill /PID 进程ID /F
```

### 4. Python版本问题
确保使用Python 3.7+版本，推荐3.8-3.11

## 🎯 开发建议

1. **开启调试模式**: 在 `config.py` 中设置 `DEBUG = True`
2. **使用虚拟环境**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **代码格式化**: 安装 Python 和 Prettier 扩展
4. **Git管理**: 使用VS Code内置的Git功能

## 📁 项目结构说明

```
library_management_project/
├── .vscode/                 # VS Code配置
│   ├── launch.json         # 调试配置
│   └── tasks.json          # 任务配置
├── templates/              # HTML模板
├── static/                 # 静态文件
├── app.py                  # 主应用文件
├── models.py               # 数据模型
├── config.py               # 配置文件
├── create_database.py      # 数据库初始化
├── run.py                  # 启动脚本
├── simple_start.py         # 简化启动脚本
└── requirements.txt        # 依赖列表
```

---

🎉 **现在您可以在VS Code中愉快地开发图书管理系统了！**