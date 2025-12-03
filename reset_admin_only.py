#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql
from datetime import datetime

def reset_database():
    print("=== 重置数据库，只保留admin管理员 ===")

    try:
        # Connect to database
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='library_management',
            charset='utf8mb4'
        )

        cursor = connection.cursor()

        # 1. 清空借阅记录表
        cursor.execute("DELETE FROM borrow_records")
        print("✓ 清空借阅记录表")

        # 2. 清空图书表
        cursor.execute("DELETE FROM books")
        print("✓ 清空图书表")

        # 3. 清空分类表
        cursor.execute("DELETE FROM categories")
        print("✓ 清空分类表")

        # 4. 清空普通用户表
        cursor.execute("DELETE FROM users")
        print("✓ 清空普通用户表")

        # 5. 清空管理员表，只保留admin
        cursor.execute("DELETE FROM admins WHERE username != 'admin'")
        print("✓ 清空管理员表，只保留admin")

        # 6. 确保admin存在
        cursor.execute("SELECT COUNT(*) FROM admins WHERE username = 'admin'")
        admin_count = cursor.fetchone()[0]

        if admin_count == 0:
            print("admin账户不存在，正在创建...")
            # 使用bcrypt的简化版本存储密码（这里用简单哈希）
            cursor.execute("""
                INSERT INTO admins (username, email, password_hash, created_at)
                VALUES ('admin', 'admin@library.com', 'admin123_hash', NOW())
            """)
            print("✓ 创建admin账户")
        else:
            print("✓ admin账户已存在")

        # 7. 重新创建默认分类
        categories = [
            ('文学小说', '各类文学作品和小说'),
            ('科学技术', '科学、技术、工程类图书'),
            ('经济管理', '经济、管理、商业类图书'),
            ('教育学习', '教材、教辅、学习资料'),
            ('艺术设计', '艺术、设计、创意类图书')
        ]

        for cat_name, cat_desc in categories:
            cursor.execute(
                "INSERT INTO categories (name, description, created_at) VALUES (%s, %s, NOW())",
                (cat_name, cat_desc)
            )

        print("✓ 创建默认分类")

        # 8. 创建示例图书
        sample_books = [
            {
                'title': 'Python编程从入门到精通',
                'author': '张三',
                'isbn': '9787111123456',
                'publisher': '清华大学出版社',
                'quantity': 5,
                'available_quantity': 5,
                'description': 'Python编程入门书籍',
                'category_id': 2
            },
            {
                'title': '活着',
                'author': '余华',
                'isbn': '9787530221234',
                'publisher': '作家出版社',
                'quantity': 3,
                'available_quantity': 3,
                'description': '余华经典小说',
                'category_id': 1
            }
        ]

        for book in sample_books:
            cursor.execute("""
                INSERT INTO books (title, author, isbn, publisher, quantity, available_quantity,
                                 description, category_id, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            """, (
                book['title'], book['author'], book['isbn'], book['publisher'],
                book['quantity'], book['available_quantity'], book['description'],
                book['category_id']
            ))

        print("✓ 创建示例图书")

        connection.commit()

        # 9. 验证结果
        print("\n=== 验证结果 ===")
        cursor.execute("SELECT id, username FROM admins")
        admins = cursor.fetchall()
        print(f"管理员数量: {len(admins)}")
        for admin in admins:
            print(f"  - {admin[1]} (ID: {admin[0]})")

        cursor.execute("SELECT id, username FROM users")
        users = cursor.fetchall()
        print(f"普通用户数量: {len(users)}")
        for user in users:
            print(f"  - {user[1]} (ID: {user[0]})")

        cursor.execute("SELECT id, title FROM books")
        books = cursor.fetchall()
        print(f"图书数量: {len(books)}")

        cursor.execute("SELECT id, name FROM categories")
        categories = cursor.fetchall()
        print(f"分类数量: {len(categories)}")

        cursor.close()
        connection.close()

        print("\n✅ 数据库重置完成！")
        print("现在只有一个管理员账户: admin")
        print("可以重新注册普通用户进行测试")

        return True

    except Exception as e:
        print(f"重置失败: {e}")
        return False

if __name__ == '__main__':
    reset_database()