#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加剩余的示例图书数据（自然科学和心理学分类）
"""

from app import app, db, Book, Category
from datetime import date

def add_remaining_books():
    """添加剩余的示例图书数据"""
    with app.app_context():
        print("开始添加剩余示例图书数据...")

        # 剩余图书数据（使用现有的分类）
        remaining_books = [
            {
                "title": "时间简史",
                "author": "史蒂芬·霍金",
                "isbn": "978-7-5357-3230-9",
                "publisher": "湖南科学技术出版社",
                "publication_date": date(2006, 1, 1),
                "quantity": 5,
                "description": "探索时间和空间核心秘密的引人入胜的故事。",
                "category_name": "科学"  # 使用现有的"科学"分类
            },
            {
                "title": "物种起源",
                "author": "查尔斯·达尔文",
                "isbn": "978-7-100-01721-1",
                "publisher": "商务印书馆",
                "publication_date": date(1995, 6, 1),
                "quantity": 3,
                "description": "达尔文论述生物进化论的重要著作。",
                "category_name": "科学"  # 使用现有的"科学"分类
            },
            {
                "title": "社会心理学",
                "author": "戴维·迈尔斯",
                "isbn": "978-7-111-36143-5",
                "publisher": "机械工业出版社",
                "publication_date": date(2011, 12, 1),
                "quantity": 5,
                "description": "系统阐述了社会心理学的理论体系和研究成果。",
                "category_name": "社会科学"  # 使用现有的"社会科学"分类
            },
            {
                "title": "心理学与生活",
                "author": "理查德·格里格",
                "isbn": "978-7-115-16383-9",
                "publisher": "人民邮电出版社",
                "publication_date": date(2003, 10, 1),
                "quantity": 4,
                "description": "心理学入门的经典教材。",
                "category_name": "社会科学"  # 使用现有的"社会科学"分类
            }
        ]

        added_count = 0
        skipped_count = 0

        for book_data in remaining_books:
            # 检查ISBN是否已存在
            existing_book = Book.query.filter_by(isbn=book_data["isbn"]).first()
            if existing_book:
                print(f"跳过已存在的图书: {book_data['title']} (ISBN: {book_data['isbn']})")
                skipped_count += 1
                continue

            # 查找对应的分类
            category = Category.query.filter_by(name=book_data["category_name"]).first()
            if not category:
                print(f"警告：未找到分类 '{book_data['category_name']}'，跳过图书 '{book_data['title']}'")
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
                category_id=category.id
            )

            db.session.add(book)
            added_count += 1
            print(f"添加图书: {book_data['title']}")

        try:
            db.session.commit()
            print(f"\n成功添加 {added_count} 本图书")
            if skipped_count > 0:
                print(f"跳过 {skipped_count} 本图书（已存在或分类不存在）")

            # 显示统计信息
            total_books = Book.query.count()
            print(f"图书馆现有图书总数: {total_books} 本")

            return True

        except Exception as e:
            db.session.rollback()
            print(f"添加图书时出错: {e}")
            return False

if __name__ == "__main__":
    print("图书管理系统 - 添加剩余示例图书数据")
    print("=" * 50)

    success = add_remaining_books()

    if success:
        print("\n剩余示例图书数据添加完成！")
        print("现在可以登录管理员账号查看和管理所有图书了")
    else:
        print("\n添加剩余示例图书数据失败")