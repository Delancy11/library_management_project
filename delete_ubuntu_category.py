#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除Ubuntu-22.04分类的脚本
"""

from app import app, db, Book, Category

def delete_ubuntu_category():
    """删除Ubuntu-22.04分类"""
    with app.app_context():
        # 查找Ubuntu-22.04分类
        ubuntu_category = Category.query.filter_by(name='Ubuntu-22.04').first()

        if not ubuntu_category:
            print("未找到Ubuntu-22.04分类")
            return False

        # 查找该分类下的所有图书
        books_in_category = Book.query.filter_by(category_id=ubuntu_category.id).all()

        if books_in_category:
            print(f"Ubuntu-22.04分类下有 {len(books_in_category)} 本图书")
            print("图书列表：")
            for book in books_in_category:
                print(f"  - 《{book.title}》 (作者: {book.author}, ISBN: {book.isbn})")

            # 查找一个默认分类（不能是Ubuntu-22.04）
            default_category = Category.query.filter(
                Category.name != 'Ubuntu-22.04'
            ).first()

            if not default_category:
                print("错误：没有其他可用的分类来转移图书")
                return False

            print(f"\n将把这些图书转移到分类: {default_category.name}")

            # 转移图书到默认分类
            for book in books_in_category:
                book.category_id = default_category.id
                print(f"  ✓ 《{book.title}》 -> {default_category.name}")

            db.session.commit()
            print(f"\n成功转移 {len(books_in_category)} 本图书")
        else:
            print("Ubuntu-22.04分类下没有图书")

        # 删除Ubuntu-22.04分类
        db.session.delete(ubuntu_category)
        db.session.commit()

        print("\n✓ Ubuntu-22.04分类删除成功！")

        # 显示删除后的分类统计
        remaining_categories = Category.query.all()
        print(f"\n当前剩余分类数量: {len(remaining_categories)}")
        print("分类列表:")
        for category in remaining_categories:
            book_count = Book.query.filter_by(category_id=category.id).count()
            print(f"  - {category.name}: {book_count} 本图书")

        return True

if __name__ == '__main__':
    print("开始删除Ubuntu-22.04分类...")
    print("=" * 50)

    try:
        success = delete_ubuntu_category()
        if success:
            print("\n" + "=" * 50)
            print("操作完成！")
        else:
            print("\n" + "=" * 50)
            print("操作失败！")
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()