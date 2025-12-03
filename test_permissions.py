#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试权限系统
"""

import os
from app import create_app
from models import db, Admin, User

def test_permissions():
    app = create_app()

    with app.app_context():
        # 测试数据库
        print("=== 数据库测试 ===")

        # 检查管理员
        admin = Admin.query.filter_by(username='admin').first()
        if admin:
            print(f"✓ 找到管理员: {admin.username} (ID: {admin.id})")
        else:
            print("❌ 未找到管理员账户")

        # 检查用户
        users = User.query.all()
        print(f"✓ 找到 {len(users)} 个用户:")
        for user in users:
            print(f"  - {user.username} (ID: {user.id}, 类型: {user.__class__.__name__})")

        # 测试权限判断
        print("\n=== 权限判断测试 ===")
        if admin:
            print(f"管理员 {admin.username}:")
            print(f"  - __class__.__name__: '{admin.__class__.__name__}'")
            print(f"  - isinstance(admin, Admin): {isinstance(admin, Admin)}")
            print(f"  - admin.__class__.__name__ == 'Admin': {admin.__class__.__name__ == 'Admin'}")

        for user in users[:3]:  # 只显示前3个用户
            print(f"\n用户 {user.username}:")
            print(f"  - __class__.__name__: '{user.__class__.__name__}'")
            print(f"  - isinstance(user, Admin): {isinstance(user, Admin)}")
            print(f"  - isinstance(user, User): {isinstance(user, User)}")
            print(f"  - user.__class__.__name__ == 'Admin': {user.__class__.__name__ == 'Admin'}")
            print(f"  - user.__class__.__name__ == 'User': {user.__class__.__name__ == 'User'}")

def create_test_user():
    """创建测试用户"""
    app = create_app()

    with app.app_context():
        # 检查是否已有测试用户
        test_user = User.query.filter_by(username='testuser').first()
        if test_user:
            print("✓ 测试用户已存在")
            return test_user

        # 创建测试用户
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

        print("✓ 创建测试用户成功")
        print("  用户名: testuser")
        print("  密码: test123")
        print("  ID:", test_user.id)

        return test_user

if __name__ == '__main__':
    print("🔧 权限系统测试")
    print("=" * 50)

    # 创建测试用户
    create_test_user()

    # 测试权限
    test_permissions()

    print("\n" + "=" * 50)
    print("📋 测试完成")
    print("\n🚀 启动应用: python run.py")
    print("👤 管理员: admin / admin123")
    print("👤 测试用户: testuser / test123")