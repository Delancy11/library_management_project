#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图书管理系统启动脚本
"""

import os
import sys
from flask import Flask
from create_database import create_database

def create_app():
    # 设置环境变量
    os.environ.setdefault('PYTHONPATH', os.path.dirname(os.path.abspath(__file__)))

    # 导入应用
    from app import app, db
    from models import Admin, User, Category, Book, BorrowRecord

    # 创建数据库
    try:
        create_database()
        print("✓ 数据库创建成功")
    except Exception as e:
        print(f"❌ 数据库创建失败: {e}")
        print("请确保MySQL服务正在运行，并且配置正确")

    # 初始化数据库表
    with app.app_context():
        try:
            db.create_all()
            print("✓ 数据库表创建成功")

            # 创建默认管理员
            if not Admin.query.filter_by(username='admin').first():
                admin = Admin(
                    username='admin',
                    email='admin@library.com'
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("✓ 默认管理员创建成功 (用户名: admin, 密码: admin123)")

            # 创建默认分类
            default_categories = [
                {'name': '文学小说', 'description': '各类文学作品和小说'},
                {'name': '科学技术', 'description': '科学、技术、工程类图书'},
                {'name': '经济管理', 'description': '经济、管理、商业类图书'},
                {'name': '教育学习', 'description': '教材、教辅、学习资料'},
                {'name': '艺术设计', 'description': '艺术、设计、创意类图书'},
                {'name': '生活健康', 'description': '生活、健康、休闲类图书'},
                {'name': '历史传记', 'description': '历史、传记、人文社科'},
                {'name': '儿童读物', 'description': '儿童、青少年读物'}
            ]

            for cat_data in default_categories:
                if not Category.query.filter_by(name=cat_data['name']).first():
                    category = Category(**cat_data)
                    db.session.add(category)

            if default_categories:
                db.session.commit()
                print("✓ 默认分类创建成功")

        except Exception as e:
            print(f"❌ 数据库初始化失败: {e}")
            return None

    return app

def main():
    print("=" * 50)
    print("📚 图书管理系统")
    print("=" * 50)

    app = create_app()
    if not app:
        print("❌ 应用创建失败")
        sys.exit(1)

    print("\n🚀 启动Web服务器...")
    print("📍 访问地址: http://localhost:5000")
    print("👤 管理员账户: admin / admin123")
    print("🔧 调试模式: 开启")
    print("-" * 50)
    print("按 Ctrl+C 停止服务器\n")

    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 服务器启动失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()