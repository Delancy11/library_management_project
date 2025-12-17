#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理Ubuntu相关分类的脚本
删除Ubuntu和Ubuntu-22.04分类，并将关联的图书转移到其他分类
"""

from app import app, db, Book, Category

def clean_ubuntu_categories():
    """清理Ubuntu相关分类"""
    with app.app_context():
        # 查找所有Ubuntu相关分类
        ubuntu_categories = Category.query.filter(
            Category.name.like('Ubuntu%')
        ).all()

        if not ubuntu_categories:
            print("未找到Ubuntu相关分类")
            return True

        print(f"找到 {len(ubuntu_categories)} 个Ubuntu相关分类:")
        for cat in ubuntu_categories:
            book_count = Book.query.filter_by(category_id=cat.id).count()
            print(f"  - {cat.name}: {book_count} 本图书")

        # 查找第一个非Ubuntu分类作为目标分类
        target_category = Category.query.filter(
            ~Category.name.like('Ubuntu%')
        ).first()

        if not target_category:
            print("错误：没有其他可用的分类来转移图书")
            return False

        print(f"\n将把所有Ubuntu分类下的图书转移到: {target_category.name}")

        total_moved = 0

        # 处理每个Ubuntu分类
        for ubuntu_category in ubuntu_categories:
            print(f"\n处理分类: {ubuntu_category.name}")

            # 查找该分类下的图书
            books = Book.query.filter_by(category_id=ubuntu_category.id).all()

            if books:
                print(f"  转移 {len(books)} 本图书")

                # 转移图书
                for book in books:
                    old_category = Category.query.get(book.category_id)
                    book.category_id = target_category.id
                    total_moved += 1
                    print(f"    ✓ 《{book.title}》 ({old_category.name} -> {target_category.name})")

            # 删除分类
            db.session.delete(ubuntu_category)
            print(f"  ✓ 删除分类: {ubuntu_category.name}")

        # 提交所有更改
        db.session.commit()

        print(f"\n" + "=" * 50)
        print("清理完成！")
        print(f"总共转移了 {total_moved} 本图书")
        print(f"删除了 {len(ubuntu_categories)} 个Ubuntu分类")

        # 显示清理后的分类统计
        remaining_categories = Category.query.order_by(Category.name).all()
        print(f"\n当前剩余分类数量: {len(remaining_categories)}")
        print("\n分类列表:")
        for category in remaining_categories:
            book_count = Book.query.filter_by(category_id=category.id).count()
            print(f"  - {category.name}: {book_count} 本图书")

        return True

def confirm_delete():
    """确认删除操作"""
    with app.app_context():
        ubuntu_categories = Category.query.filter(
            Category.name.like('Ubuntu%')
        ).all()

        if not ubuntu_categories:
            print("没有找到Ubuntu相关分类")
            return True

        print("即将删除以下Ubuntu相关分类:")
        total_books = 0
        for cat in ubuntu_categories:
            book_count = Book.query.filter_by(category_id=cat.id).count()
            total_books += book_count
            print(f"  - {cat.name} ({book_count} 本图书)")

        print(f"\n总计: {len(ubuntu_categories)} 个分类, {total_books} 本图书")
        print("\n这些图书将被转移到第一个可用的非Ubuntu分类")

        confirm = input("\n确定要继续吗？(yes/no): ")
        return confirm.lower() in ['yes', 'y', '是']

if __name__ == '__main__':
    print("Ubuntu分类清理工具")
    print("=" * 50)

    if confirm_delete():
        try:
            success = clean_ubuntu_categories()
            if success:
                print("\n操作成功完成！")
            else:
                print("\n操作失败！")
        except Exception as e:
            print(f"\n错误: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("操作已取消")