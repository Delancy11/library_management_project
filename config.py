import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    # 使用SQLite数据库，避免MySQL配置问题
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///library.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 管理员配置
    ADMIN_DEFAULT_PASSWORD = 'admin123'

    # 分页配置
    BOOKS_PER_PAGE = 10
    RECORDS_PER_PAGE = 10