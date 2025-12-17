#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加最终的示例图书数据
"""

from app import app, db, Book, Category
from datetime import date

def add_final_books():
    """添加最终的示例图书数据"""
    with app.app_context():
        print("开始添加最终示例图书数据...")

        # 最终图书数据
        final_books = [
            {
                "title": "时间简史",
                "author": "史蒂芬·霍金",
                "isbn": "978-7-5357-3230-9",
                "publisher": "湖南科学技术出版社",
                "publication_date": date(2006, 1, 1),
                "quantity": 5,
                "description": "探索时间和空间核心秘密的引人入胜的故事。",
                "category_id": 4  # 科学分类
            },
            {
                "title": "物种起源",
                "author": "查尔斯·达尔文",
                "isbn": "978-7-100-01721-1",
                "publisher": "商务印书馆",
                "publication_date": date(1995, 6, 1),
                "quantity": 3,
                "description": "达尔文论述生物进化论的重要著作。",
                "category_id": 4  # 科学分类
            },
            {
                "title": "宇宙简史",
                "author": "史蒂芬·霍金",
                "isbn": "978-7-5357-7230-1",
                "publisher": "湖南科学技术出版社",
                "publication_date": date(2012, 1, 1),
                "quantity": 4,
                "description": "从大爆炸到黑洞，霍金带你探索宇宙的奥秘。",
                "category_id": 4  # 科学分类
            },
            {
                "title": "自私的基因",
                "author": "理查德·道金斯",
                "isbn": "978-7-5086-3594-5",
                "publisher": "中信出版社",
                "publication_date": date(2012, 9, 1),
                "quantity": 3,
                "description": "从基因的角度重新审视生命和进化。",
                "category_id": 4  # 科学分类
            }
        ]

        added_count = 0
        skipped_count = 0

        for book_data in final_books:
            # 检查ISBN是否已存在
            existing_book = Book.query.filter_by(isbn=book_data["isbn"]).first()
            if existing_book:
                print(f"跳过已存在的图书: {book_data['title']}")
                skipped_count += 1
                continue

            # 创建图书对象
            book = Book(
                title=book_data["title"],
                author=book_data["author"],
                isbn=book_data["isbn"],
                publisher=book_data["publisher"],
                publication_date=book_data["publication_date"],
                quantity=book_data["quantity"],
                available_quantity=book_data["quantity"],
                description=book_data["description"],
                category_id=book_data["category_id"]
            )

            db.session.add(book)
            added_count += 1
            print(f"添加图书: {book_data['title']}")

        try:
            db.session.commit()
            print(f"\n成功添加 {added_count} 本图书")
            if skipped_count > 0:
                print(f"跳过 {skipped_count} 本图书（已存在）")

            # 显示统计信息
            total_books = Book.query.count()
            print(f"图书馆现有图书总数: {total_books} 本")

            return True

        except Exception as e:
            db.session.rollback()
            print(f"添加图书时出错: {e}")
            return False

if __name__ == "__main__":
    print("图书管理系统 - 添加最终示例图书数据")
    print("=" * 50)

    success = add_final_books()

    if success:
        print("\n最终示例图书数据添加完成！")
        print("现在可以登录管理员账号查看和管理所有图书了")
        print("\n管理员登录信息:")
        print("用户名: admin")
        print("密码: admin123")
    else:
        print("\n添加最终示例图书数据失败")