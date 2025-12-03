#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql

def clean_database():
    print("=== Cleaning database, keeping only admin ===")

    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='library_management',
            charset='utf8mb4'
        )

        cursor = connection.cursor()

        # Clear all tables except admin
        cursor.execute("DELETE FROM borrow_records")
        cursor.execute("DELETE FROM books")
        cursor.execute("DELETE FROM categories")
        cursor.execute("DELETE FROM users")
        cursor.execute("DELETE FROM admins WHERE username != 'admin'")

        print("Tables cleared")

        # Ensure admin exists
        cursor.execute("SELECT COUNT(*) FROM admins WHERE username = 'admin'")
        admin_count = cursor.fetchone()[0]

        if admin_count == 0:
            cursor.execute("""
                INSERT INTO admins (username, email, password_hash, created_at)
                VALUES ('admin', 'admin@library.com', 'pbkdf2:sha256:260000$salt$hash', NOW())
            """)
            print("Admin account created")

        # Create categories
        categories = [
            ('文学小说', '文学作品'),
            ('科学技术', '技术类'),
            ('经济管理', '经济管理类'),
            ('教育学习', '教育类')
        ]

        for cat_name, cat_desc in categories:
            cursor.execute(
                "INSERT INTO categories (name, description, created_at) VALUES (%s, %s, NOW())",
                (cat_name, cat_desc)
            )

        print("Categories created")

        # Get first category ID for foreign key
        cursor.execute("SELECT id FROM categories LIMIT 1")
        category_id = cursor.fetchone()[0]

        # Create sample books
        cursor.execute("""
            INSERT INTO books (title, author, isbn, publisher, quantity, available_quantity,
                             description, category_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
        """, ('Python编程', '张三', '9787111123456', '清华大学出版社', 5, 5, 'Python书籍', category_id))

        print("Sample books created")

        connection.commit()

        # Verify
        cursor.execute("SELECT username FROM admins")
        admins = cursor.fetchall()
        cursor.execute("SELECT username FROM users")
        users = cursor.fetchall()

        print(f"Admins: {[a[0] for a in admins]}")
        print(f"Users: {[u[0] for u in users]}")

        cursor.close()
        connection.close()
        print("Database reset complete!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    clean_database()