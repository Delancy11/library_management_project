#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQLite数据库初始化脚本
"""

import os
import sys
from werkzeug.security import generate_password_hash
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # 导入Flask应用和模型
    from app import app, db
    from models import Admin, User, Category, Book, BorrowRecord

    def init_database():
        """初始化SQLite数据库"""
        print("正在初始化SQLite数据库...")

        with app.app_context():
            # 删除所有表（如果存在）
            db.drop_all()
            print("清理旧数据库表...")

            # 创建所有表
            db.create_all()
            print("创建数据库表成功！")

            # 检查是否已有管理员
            if not Admin.query.first():
                print("创建默认管理员账户...")
                admin = Admin(
                    username='admin',
                    email='admin@library.com'
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("默认管理员账户创建成功: admin / admin123")

            # 添加默认分类
            if not Category.query.first():
                print("添加默认图书分类...")
                categories = [
                    {'name': '计算机科学', 'description': '计算机科学与技术类图书'},
                    {'name': '文学', 'description': '文学作品类图书'},
                    {'name': '历史', 'description': '历史类图书'},
                    {'name': '哲学', 'description': '哲学类图书'},
                    {'name': '数学', 'description': '数学类图书'},
                    {'name': '物理学', 'description': '物理学类图书'},
                    {'name': '化学', 'description': '化学类图书'},
                    {'name': '生物学', 'description': '生物学类图书'},
                    {'name': '经济学', 'description': '经济学类图书'},
                    {'name': '艺术', 'description': '艺术类图书'}
                ]

                for cat_data in categories:
                    category = Category(name=cat_data['name'], description=cat_data['description'])
                    db.session.add(category)

                db.session.commit()
                print("默认分类添加完成")

            # 添加一些示例图书
            if not Book.query.first():
                print("添加示例图书...")

                # 获取计算机科学分类
                computer_cat = Category.query.filter_by(name='计算机科学').first()
                literature_cat = Category.query.filter_by(name='文学').first()

                sample_books = [
                    {
                        'title': 'Python编程：从入门到实践',
                        'author': '埃里克·马瑟斯',
                        'isbn': '9787115546081',
                        'category': computer_cat,
                        'publisher': '人民邮电出版社',
                        'pages': 459,
                        'description': '一本针对所有层次的Python读者而作的Python入门书',
                        'total_copies': 3,
                        'available_copies': 3
                    },
                    {
                        'title': 'Flask Web开发：基于Python的Web应用开发实战',
                        'author': '米格尔·格林贝格',
                        'isbn': '9787115428500',
                        'category': computer_cat,
                        'publisher': '人民邮电出版社',
                        'pages': 320,
                        'description': '全面介绍Flask框架的使用',
                        'total_copies': 2,
                        'available_copies': 2
                    },
                    {
                        'title': '算法导论',
                        'author': '托马斯·科尔曼',
                        'isbn': '9787111407010',
                        'category': computer_cat,
                        'publisher': '机械工业出版社',
                        'pages': 780,
                        'description': '计算机算法领域的经典教材',
                        'total_copies': 2,
                        'available_copies': 2
                    },
                    {
                        'title': '红楼梦',
                        'author': '曹雪芹',
                        'isbn': '9787020002207',
                        'category': literature_cat,
                        'publisher': '人民文学出版社',
                        'pages': 1200,
                        'description': '中国古典文学四大名著之一',
                        'total_copies': 5,
                        'available_copies': 5
                    }
                ]

                for book_data in sample_books:
                    book = Book(
                        title=book_data['title'],
                        author=book_data['author'],
                        isbn=book_data['isbn'],
                        category_id=book_data['category'].id,
                        publisher=book_data['publisher'],
                        description=book_data['description'],
                        quantity=book_data['total_copies'],
                        available_quantity=book_data['available_copies']
                    )
                    db.session.add(book)

                db.session.commit()
                print("示例图书添加完成")

            # 添加一个测试用户
            if not User.query.first():
                print("创建测试用户账户...")
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
                print("测试用户账户创建成功: testuser / test123")

            print("SQLite数据库初始化完成！")
            print("数据库文件位置: library.db")

            # 显示统计信息
            print("数据库统计:")
            print(f"   管理员数量: {Admin.query.count()}")
            print(f"   用户数量: {User.query.count()}")
            print(f"   分类数量: {Category.query.count()}")
            print(f"   图书数量: {Book.query.count()}")

    if __name__ == "__main__":
        print("=" * 50)
        print("图书管理系统 - SQLite数据库初始化")
        print("=" * 50)
        init_database()
        print("=" * 50)

except ImportError as e:
    print(f"导入错误: {e}")
    print("请先安装Flask相关依赖包:")
    print("   pip install flask flask-sqlalchemy flask-login")
except Exception as e:
    print(f"初始化失败: {e}")
    import traceback
    traceback.print_exc()