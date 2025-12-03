import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:123456@localhost/library_management'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 管理员配置
    ADMIN_DEFAULT_PASSWORD = 'admin123'

    # 分页配置
    BOOKS_PER_PAGE = 10
    RECORDS_PER_PAGE = 10