#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重建数据库脚本
"""

import pymysql
import os
from models import db, Admin, User, Category, Book, BorrowRecord

def create_database():
    """创建数据库"""
    print("正在创建数据库...")

    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '123456',
        'charset': 'utf8mb4'
    }

    try:
        connection = pymysql.connect(**config)
        cursor = connection.cursor()

        # 删除数据库
        cursor.execute("DROP DATABASE IF EXISTS library_management")
        print("  - 删除旧数据库")

        # 创建数据库
        cursor.execute("CREATE DATABASE library_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("  - 创建新数据库")

        cursor.close()
        connection.close()
        print("✓ 数据库创建完成")
        return True
    except Exception as e:
        print(f"❌ 数据库创建失败: {e}")
        return False

def init_database():
    """初始化数据库"""
    from app import create_app

    app = create_app()

    with app.app_context():
        try:
            # 创建表
            db.create_all()
            print("✓ 数据库表创建完成")

            # 创建管理员
            if not Admin.query.filter_by(username='admin').first():
                admin = Admin(username='admin', email='admin@library.com')
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("✓ 创建管理员账户")

            # 创建分类
            categories = [
                {'name': '文学小说', 'description': '各类文学作品和小说'},
                {'name': '科学技术', 'description': '科学、技术、工程类图书'},
                {'name': '经济管理', 'description': '经济、管理、商业类图书'},
                {'name': '教育学习', 'description': '教材、教辅、学习资料'},
                {'name': '艺术设计', 'description': '艺术、设计、创意类图书'},
                {'name': '生活健康', 'description': '生活、健康、休闲类图书'},
                {'name': '历史传记', 'description': '历史、传记、人文社科'},
                {'name': '儿童读物', 'description': '儿童、青少年读物'}
            ]

            for cat_data in categories:
                if not Category.query.filter_by(name=cat_data['name']).first():
                    category = Category(**cat_data)
                    db.session.add(category)

            db.session.commit()
            print(f"✓ 创建 {len(categories)} 个分类")

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
                print("✓ 创建测试用户账户")

            # 创建示例图书
            books_data = [
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

            for book_data in books_data:
                if not Book.query.filter_by(isbn=book_data['isbn']).first():
                    book = Book(**book_data)
                    db.session.add(book)

            db.session.commit()
            print(f"✓ 创建 {len(books_data)} 本示例图书")

            print("\n=== 数据库初始化完成 ===")
            print("管理员账户: admin / admin123")
            print("测试用户: testuser / test123")
            print("分类数量:", len(Category.query.all()))
            print("图书数量:", len(Book.query.all()))
            print("用户数量:", len(User.query.all()))

            return True

        except Exception as e:
            print(f"❌ 数据库初始化失败: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    print("=" * 50)
    print("重建数据库")
    print("=" * 50)

    # 创建数据库
    if not create_database():
        print("❌ 数据库创建失败，停止执行")
        return

    # 初始化数据库
    if not init_database():
        print("❌ 数据库初始化失败")
        return

    print("\n" + "=" * 50)
    print("数据库重建完成！")
    print("现在可以启动应用: python start_server.py")

if __name__ == '__main__':
    main()