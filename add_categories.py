#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql

def add_categories():
    print("Adding categories to database...")
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

        # Check existing categories
        cursor.execute("SELECT COUNT(*) FROM categories")
        category_count = cursor.fetchone()[0]
        print(f"Found {category_count} existing categories")

        # Default categories
        default_categories = [
            ('文学小说', '各类文学作品和小说'),
            ('科学技术', '科学、技术、工程类图书'),
            ('经济管理', '经济、管理、商业类图书'),
            ('教育学习', '教材、教辅、学习资料'),
            ('艺术设计', '艺术、设计、创意类图书'),
            ('生活健康', '生活、健康、休闲类图书'),
            ('历史传记', '历史、传记、人文社科'),
            ('儿童读物', '儿童、青少年读物')
        ]

        # Insert categories
        for cat_name, cat_desc in default_categories:
            cursor.execute(
                "INSERT IGNORE INTO categories (name, description, created_at) VALUES (%s, %s, NOW())",
                (cat_name, cat_desc)
            )
            print(f"Added category: {cat_name}")

        connection.commit()

        # Show all categories
        cursor.execute("SELECT id, name FROM categories ORDER BY id")
        categories = cursor.fetchall()
        print("\nAll categories:")
        for cat in categories:
            print(f"  ID {cat[0]}: {cat[1]}")

        cursor.close()
        connection.close()
        print("Categories added successfully!")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == '__main__':
    if add_categories():
        print("\nNow you can add books with category dropdown!")
    else:
        print("Failed to add categories")