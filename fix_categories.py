#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix categories issue
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pymysql
from config import Config

# 创建数据库连接
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        database='library_management',
        charset='utf8mb4'
    )

def fix_categories():
    print("=== Fix Categories ===")
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if categories table exists and has data
        cursor.execute("SELECT COUNT(*) FROM categories")
        category_count = cursor.fetchone()[0]
        print(f"Found {category_count} categories in database")

        # Create default categories if table is empty
        if category_count == 0:
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

            for cat_name, cat_desc in default_categories:
                cursor.execute(
                    "INSERT INTO categories (name, description, created_at) VALUES (%s, %s, NOW())",
                    (cat_name, cat_desc)
                )
                print(f"Created category: {cat_name}")

            connection.commit()
            print(f"Created {len(default_categories)} default categories")

        # Show all categories
        cursor.execute("SELECT id, name, description FROM categories ORDER BY id")
        categories = cursor.fetchall()
        print("\nAll categories:")
        for cat in categories:
            print(f"  - {cat[0]}: {cat[1]}")

        cursor.close()
        connection.close()
        print("Categories fix completed!")
        return True

    except Exception as e:
        print(f"Error fixing categories: {e}")
        import traceback
        traceback.print_exc()
        return False

def fix_categories():
    app = create_app()

    with app.app_context():
        try:
            # Check if categories exist
            existing_categories = Category.query.all()
            print(f"Found {len(existing_categories)} categories in database")

            if not existing_categories:
                # Create default categories
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
                        print(f"Created category: {cat_data['name']}")

                db.session.commit()
                print("Default categories created successfully!")
            else:
                for cat in existing_categories:
                    print(f"  - {cat.name} (ID: {cat.id})")

            print(f"\nTotal categories: {len(Category.query.all())}")
            return True

        except Exception as e:
            print(f"Error fixing categories: {e}")
            return False

if __name__ == '__main__':
    print("=== Fix Categories Issue ===")
    if fix_categories():
        print("Categories fix completed!")
        print("You can now add books with proper category dropdown.")
    else:
        print("Categories fix failed!")