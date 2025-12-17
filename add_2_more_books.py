#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加2本额外图书以达到20本的目标
"""

from app import app, db, Book, Category
from datetime import date

def add_2_more_books():
    """添加2本额外图书"""
    with app.app_context():
        print("开始添加2本额外图书...")

        # 找到计算机科学分类
        computer_category = Category.query.filter_by(name='计算机科学').first()
        if not computer_category:
            print("错误：未找到计算机科学分类")
            return False

        # 2本额外图书
        additional_books = [
            {
                "title": "机器学习实战",
                "author": "Peter Harrington",
                "isbn": "978-7-115-31795-7",
                "publisher": "人民邮电出版社",
                "publication_date": date(2013, 6, 1),
                "quantity": 3,
                "description": "通过精心编排的实例，切入日常工作任务，摒弃学术化语言，利用高效的可复用Python代码来阐释机器学习的基础算法。",
                "category_id": computer_category.id
            },
            {
                "title": "深度学习",
                "author": "Ian Goodfellow",
                "isbn": "978-7-115-46147-6",
                "publisher": "人民邮电出版社",
                "publication_date": date(2017, 8, 1),
                "quantity": 2,
                "description": "AI圣经！深度学习领域奠基性的经典教材！全书的内容包括3个部分：第1部分介绍基本的数学工具和机器学习的概念，第2部分系统深入地讲解现今已成熟的深度学习方法和技术，第3部分讨论某些具有前瞻性的方向和想法。",
                "category_id": computer_category.id
            }
        ]

        success_count = 0
        for book_data in additional_books:
            # 检查ISBN是否已存在
            existing_book = Book.query.filter_by(isbn=book_data['isbn']).first()
            if existing_book:
                print(f"图书已存在: {existing_book.title} (ISBN: {existing_book.isbn})")
                continue

            # 创建新书
            book = Book(
                title=book_data['title'],
                author=book_data['author'],
                isbn=book_data['isbn'],
                publisher=book_data['publisher'],
                publication_date=book_data['publication_date'],
                quantity=book_data['quantity'],
                available_quantity=book_data['quantity'],
                description=book_data['description'],
                category_id=book_data['category_id']
            )

            db.session.add(book)
            success_count += 1
            print(f"添加图书: {book.title}")

        try:
            db.session.commit()
            print(f"成功添加 {success_count} 本图书")

            # 检查总数
            total_books = Book.query.count()
            print(f"数据库中图书总数: {total_books} 本")

            return True
        except Exception as e:
            db.session.rollback()
            print(f"添加图书时出错: {e}")
            return False

if __name__ == '__main__':
    if add_2_more_books():
        print("2本额外图书添加完成！现在你有20本图书了！")
    else:
        print("添加图书失败")