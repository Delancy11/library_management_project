#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VS Code 图书管理系统启动脚本
解决 VS Code 中无法运行的问题
"""

import os
import sys

# 设置控制台编码
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def main():
    print("=" * 50)
    print("图书管理系统 - VS Code 版本")
    print("=" * 50)

    # 获取当前脚本目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    print(f"工作目录: {current_dir}")

    # 添加到 Python 路径
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

    try:
        # 导入应用和数据库
        from app import app
        from models import db

        print("正在初始化数据库...")
        with app.app_context():
            # 创建所有表
            db.create_all()
            print("[OK] 数据库表创建成功")

            # 检查是否有管理员
            from models import Admin
            if not Admin.query.first():
                print("正在创建默认管理员...")
                admin = Admin(
                    username='admin',
                    email='admin@library.com'
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("[OK] 默认管理员创建成功 (admin/admin123)")

            # 检查是否有测试用户
            from models import User
            if not User.query.filter_by(username='testuser').first():
                print("正在创建测试用户...")
                test_user = User(
                    username='testuser',
                    email='test@example.com',
                    full_name='测试用户',
                    phone='13800138000',
                    address='测试地址'
                )
                test_user.set_password('test123')
                db.session.add(test_user)
                db.session.commit()
                print("[OK] 测试用户创建成功 (testuser/test123)")

            # 检查是否有分类
            from models import Category
            if not Category.query.first():
                print("正在创建默认分类...")
                default_categories = [
                    {'name': '文学小说', 'description': '各类文学作品和小说'},
                    {'name': '科学技术', 'description': '科学、技术、工程类图书'},
                    {'name': '经济管理', 'description': '经济、管理、商业类图书'},
                    {'name': '教育学习', 'description': '教材、教辅、学习资料'},
                    {'name': '艺术设计', 'description': '艺术、设计、创意类图书'}
                ]

                for cat_data in default_categories:
                    category = Category(**cat_data)
                    db.session.add(category)

                db.session.commit()
                print("✓ 默认分类创建成功")

        print("\n" + "=" * 50)
        print("启动信息:")
        print(f"访问地址: http://localhost:5000")
        print(f"管理员账号: admin / admin123")
        print(f"测试用户: testuser / test123")
        print("=" * 50)
        print("\n正在启动服务器...")
        print("按 Ctrl+C 停止服务器\n")

        # 启动 Flask 应用
        app.run(
            host='127.0.0.1',  # 使用 localhost
            port=5000,
            debug=True
        )

    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保已安装所有依赖包:")
        print("pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())