#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为图书管理系统添加示例图书数据的脚本
"""

from app import app, db, Book, Category
from datetime import datetime, date

def add_sample_books():
    """添加示例图书数据"""
    with app.app_context():
        print("开始添加示例图书数据...")

        # 检查数据库中是否已有分类数据
        categories = Category.query.all()
        if not categories:
            print("警告：数据库中没有分类数据，请先运行 add_categories.py")
            return False

        # 示例图书数据
        sample_books = [
            {
                "title": "Python编程：从入门到实践",
                "author": "埃里克·马瑟斯",
                "isbn": "978-7-115-42802-8",
                "publisher": "人民邮电出版社",
                "publication_date": date(2016, 7, 1),
                "quantity": 5,
                "description": "一本针对所有层次的Python读者而作的Python入门书，旨在帮助读者快速掌握Python编程的基础知识。",
                "category_name": "计算机科学"
            },
            {
                "title": "算法导论",
                "author": "Thomas H. Cormen",
                "isbn": "978-7-111-40701-0",
                "publisher": "机械工业出版社",
                "publication_date": date(2012, 7, 1),
                "quantity": 3,
                "description": "计算机算法领域的经典教材，全面介绍了算法的设计与分析。",
                "category_name": "计算机科学"
            },
            {
                "title": "深入理解计算机系统",
                "author": "Randal E. Bryant",
                "isbn": "978-7-111-32133-0",
                "publisher": "机械工业出版社",
                "publication_date": date(2011, 1, 1),
                "quantity": 4,
                "description": "从程序员的视角详细阐述计算机系统的本质概念。",
                "category_name": "计算机科学"
            },
            {
                "title": "红楼梦",
                "author": "曹雪芹",
                "isbn": "978-7-02-002207-0",
                "publisher": "人民文学出版社",
                "publication_date": date(1996, 12, 1),
                "quantity": 8,
                "description": "中国古典文学四大名著之一，描绘了封建社会的人性美和悲剧美。",
                "category_name": "文学"
            },
            {
                "title": "活着",
                "author": "余华",
                "isbn": "978-7-5063-9179-3",
                "publisher": "作家出版社",
                "publication_date": date(2012, 8, 1),
                "quantity": 6,
                "description": "讲述了农村人福贵悲惨的人生遭遇，反映了大时代下普通人的命运。",
                "category_name": "文学"
            },
            {
                "title": "百年孤独",
                "author": "加西亚·马尔克斯",
                "isbn": "978-7-5442-5865-7",
                "publisher": "南海出版公司",
                "publication_date": date(2011, 6, 1),
                "quantity": 4,
                "description": "魔幻现实主义文学的代表作，描述了布恩迪亚家族七代人的传奇故事。",
                "category_name": "文学"
            },
            {
                "title": "时间简史",
                "author": "史蒂芬·霍金",
                "isbn": "978-7-5357-3230-9",
                "publisher": "湖南科学技术出版社",
                "publication_date": date(2006, 1, 1),
                "quantity": 5,
                "description": "探索时间和空间核心秘密的引人入胜的故事。",
                "category_name": "自然科学"
            },
            {
                "title": "物种起源",
                "author": "查尔斯·达尔文",
                "isbn": "978-7-100-01721-1",
                "publisher": "商务印书馆",
                "publication_date": date(1995, 6, 1),
                "quantity": 3,
                "description": "达尔文论述生物进化论的重要著作。",
                "category_name": "自然科学"
            },
            {
                "title": "人类简史",
                "author": "尤瓦尔·赫拉利",
                "isbn": "978-7-5086-4735-7",
                "publisher": "中信出版社",
                "publication_date": date(2014, 11, 1),
                "quantity": 7,
                "description": "从石器时代到21世纪的人类发展史。",
                "category_name": "历史"
            },
            {
                "title": "万历十五年",
                "author": "黄仁宇",
                "isbn": "978-7-108-00982-1",
                "publisher": "生活·读书·新知三联书店",
                "publication_date": date(1997, 5, 1),
                "quantity": 4,
                "description": "以1587年为横断面，剖析中国社会的传统管理模式。",
                "category_name": "历史"
            },
            {
                "title": "经济学原理",
                "author": "N.格里高利·曼昆",
                "isbn": "978-7-301-12684-3",
                "publisher": "北京大学出版社",
                "publication_date": date(2009, 4, 1),
                "quantity": 6,
                "description": "世界上最流行的经济学教材之一。",
                "category_name": "经济学"
            },
            {
                "title": "国富论",
                "author": "亚当·斯密",
                "isbn": "978-7-100-00957-9",
                "publisher": "商务印书馆",
                "publication_date": date(1972, 12, 1),
                "quantity": 3,
                "description": "现代经济学的奠基之作。",
                "category_name": "经济学"
            },
            {
                "title": "社会心理学",
                "author": "戴维·迈尔斯",
                "isbn": "978-7-111-36143-5",
                "publisher": "机械工业出版社",
                "publication_date": date(2011, 12, 1),
                "quantity": 5,
                "description": "系统阐述了社会心理学的理论体系和研究成果。",
                "category_name": "心理学"
            },
            {
                "title": "心理学与生活",
                "author": "理查德·格里格",
                "isbn": "978-7-115-16383-9",
                "publisher": "人民邮电出版社",
                "publication_date": date(2003, 10, 1),
                "quantity": 4,
                "description": "心理学入门的经典教材。",
                "category_name": "心理学"
            }
        ]

        added_count = 0
        skipped_count = 0

        for book_data in sample_books:
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
            print(f"❌ 添加图书时出错: {e}")
            return False

def show_books_by_category():
    """按分类显示图书统计"""
    with app.app_context():
        print("\n各分类图书统计:")
        print("-" * 50)

        categories = Category.query.all()
        for category in categories:
            book_count = Book.query.filter_by(category_id=category.id).count()
            if book_count > 0:
                print(f"{category.name}: {book_count} 本")

if __name__ == "__main__":
    print("图书管理系统 - 添加示例图书数据")
    print("=" * 50)

    success = add_sample_books()

    if success:
        show_books_by_category()
        print("\n示例图书数据添加完成！")
        print("现在可以登录管理员账号查看和管理这些图书了")
    else:
        print("\n添加示例图书数据失败")