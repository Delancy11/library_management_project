#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理和重建数据库
"""

import pymysql
from create_database import config
from models import db, Admin, User, Category, Book, BorrowRecord
from config import Config

def clean_database():
    """清理数据库"""
    print("🔧 清理数据库...")

    try:
        # 连接MySQL
        connection = pymysql.connect(**config)
        cursor = connection.cursor()

        # 删除数据库
        cursor.execute("DROP DATABASE IF EXISTS library_management")
        print("✓ 删除旧数据库")

        # 重新创建数据库
        cursor.execute("CREATE DATABASE library_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("✓ 创建新数据库")

        cursor.close()
        connection.close()

        print("✓ 数据库清理完成")

    except Exception as e:
        print(f"❌ 数据库清理失败: {e}")
        return False

    return True

def init_sample_data():
    """初始化示例数据"""
    from app import create_app

    app = create_app()

    with app.app_context():
        try:
            # 创建表
            db.create_all()
            print("✓ 创建数据表")

            # 创建管理员（ID固定为1）
            admin = Admin(username='admin', email='admin@library.com')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print(f"✓ 创建管理员: admin (ID: {admin.id})")

            # 创建分类
            categories = [
                {'name': '文学小说', 'description': '各类文学作品和小说'},
                {'name': '科学技术', 'description': '科学、技术、工程类图书'},
                {'name': '经济管理', 'description': '经济、管理、商业类图书'},
                {'name': '教育学习', 'description': '教材、教辅、学习资料'},
                {'name': '艺术设计', 'description': '艺术、设计、创意类图书'}
            ]

            for cat_data in categories:
                category = Category(**cat_data)
                db.session.add(category)

            db.session.commit()
            print(f"✓ 创建 {len(categories)} 个分类")

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
                },
                {
                    'title': '经济学原理',
                    'author': '曼昆',
                    'isbn': '9787301123456',
                    'publisher': '北京大学出版社',
                    'quantity': 4,
                    'available_quantity': 4,
                    'description': '经济学基础教材',
                    'category_id': 3
                }
            ]

            for book_data in books_data:
                book = Book(**book_data)
                db.session.add(book)

            db.session.commit()
            print(f"✓ 创建 {len(books_data)} 本示例图书")

            # 创建测试用户
            test_user = User(
                username='testuser',
                email='test@example.com',
                full_name='测试用户',
                phone='13800138000',
                address='北京市海淀区'
            )
            test_user.set_password('test123')
            db.session.add(test_user)
            db.session.commit()
            print(f"✓ 创建测试用户: testuser (ID: {test_user.id})")

            print("✓ 示例数据初始化完成")
            return True

        except Exception as e:
            print(f"❌ 数据初始化失败: {e}")
            return False

def main():
    print("=" * 50)
    print("🗃️ 图书管理系统 - 数据库清理和初始化")
    print("=" * 50)

    # 清理数据库
    if not clean_database():
        print("❌ 数据库清理失败，停止执行")
        return

    print("\n" + "-" * 30)

    # 初始化数据
    if not init_sample_data():
        print("❌ 数据初始化失败")
        return

    print("\n" + "=" * 50)
    print("🎉 数据库重建成功！")
    print("\n📋 可用账户:")
    print("👤 管理员: admin / admin123")
    print("👤 测试用户: testuser / test123")
    print("\n🚀 启动应用: python run.py")
    print("🌐 访问地址: http://localhost:5000")

if __name__ == '__main__':
    main()