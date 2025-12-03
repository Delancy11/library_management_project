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

    # 创建数据库
    try:
        create_database()
        print("数据库创建成功")
    except Exception as e:
        print(f"数据库创建失败: {e}")
        print("请确保MySQL服务正在运行，并且配置正确")
        return None

    # 导入应用
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from app import app, initialize_database
    from models import db, Admin, User, Category, Book, BorrowRecord

    # 初始化数据库表和基础数据
    if not initialize_database():
        print("❌ 数据库初始化失败")
        return None

    # 检查分类是否存在
    import pymysql
    try:
        connection = pymysql.connect(
                host='localhost',
                user='root',
                password='123456',
                database='library_management',
                charset='utf8mb4'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM categories")
        category_count = cursor.fetchone()[0]
        cursor.close()
        connection.close()

        if category_count == 0:
            print("分类表为空，正在添加分类...")
            from add_categories import add_categories
            if not add_categories():
                print("❌ 分类添加失败")
                return None
        else:
            print(f"数据库包含 {category_count} 个分类")

    except Exception as e:
        print(f"检查分类失败: {e}")
        return None

    with app.app_context():
        try:
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

            # 创建测试用户
            if not User.query.filter_by(username='testuser').first():
                test_user = User(
                    username='testuser',
                    email='test@example.com',
                    full_name='测试用户',
                    phone='13800138000',
                    address='测试地址'
                )
                test_user.set_password('test123')
                db.session.add(test_user)
                db.session.commit()
                print("✓ 测试用户创建成功 (用户名: testuser, 密码: test123)")

            # 创建示例图书
            if not Book.query.first():
                sample_books = [
                    {
                        'title': 'Python编程从入门到精通',
                        'author': '张三',
                        'isbn': '9787111123456',
                        'publisher': '清华大学出版社',
                        'quantity': 5,
                        'available_quantity': 5,
                        'description': 'Python编程入门书籍，适合初学者',
                        'category_id': 2
                    },
                    {
                        'title': '活着',
                        'author': '余华',
                        'isbn': '9787530221234',
                        'publisher': '作家出版社',
                        'quantity': 3,
                        'available_quantity': 3,
                        'description': '余华经典小说作品',
                        'category_id': 1
                    }
                ]

                for book_data in sample_books:
                    book = Book(**book_data)
                    db.session.add(book)

                db.session.commit()
                print("✓ 示例图书创建成功")

        except Exception as e:
            print(f"❌ 示例数据创建失败: {e}")

    return app

def main():
    print("=" * 50)
    print("图书管理系统")
    print("=" * 50)

    app = create_app()
    if not app:
        print("❌ 应用创建失败")
        sys.exit(1)

    print("\n启动Web服务器...")
    print("访问地址: http://localhost:5000")
    print("管理员账户: admin / admin123")
    print("测试用户: testuser / test123")
    print("调试模式: 开启")
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