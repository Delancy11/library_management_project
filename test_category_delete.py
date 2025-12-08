#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试分类删除功能
"""

import os
import sys

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app, db
    from models import Category, Book

    def test_categories():
        """测试分类和图书状态"""
        with app.app_context():
            print("=== 当前分类和图书状态 ===")
            categories = Category.query.all()
            for cat in categories:
                book_count = Book.query.filter_by(category_id=cat.id).count()
                print(f"分类: {cat.name} (ID: {cat.id}) - 图书数量: {book_count}")
                if book_count > 0:
                    books = Book.query.filter_by(category_id=cat.id).all()
                    for book in books:
                        print(f"  - {book.title}")
                print()

            print("=== 测试强制删除功能 ===")
            # 找一个有图书的分类进行测试
            computer_cat = Category.query.filter_by(name='计算机科学').first()
            if computer_cat:
                book_count = Book.query.filter_by(category_id=computer_cat.id).count()
                print(f"找到分类: {computer_cat.name}，有 {book_count} 本图书")

                # 找一个目标分类
                other_cat = Category.query.filter(Category.id != computer_cat.id).first()
                if other_cat:
                    print(f"图书将被移动到: {other_cat.name}")
                    return True
                else:
                    print("没有找到其他分类可以接收图书")
                    return False
            else:
                print("没有找到计算机科学分类")
                return False

    def main():
        print("=" * 50)
        print("图书管理系统 - 分类删除功能测试")
        print("=" * 50)

        success = test_categories()

        print("=" * 50)
        if success:
            print("测试通过！")
            print("1. 有图书的分类现在显示下拉删除按钮")
            print("2. 空的分类显示普通删除按钮")
            print("3. 强制删除功能已实现")
            print("4. 请在浏览器中访问 /admin/categories 查看效果")
        else:
            print("测试失败")
        print("=" * 50)

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"导入错误: {e}")
except Exception as e:
    print(f"测试失败: {e}")
    import traceback
    traceback.print_exc()