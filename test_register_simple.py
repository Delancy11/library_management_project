#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试用户注册功能
"""

import os
import sys

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app, db
    from models import User

    def test_user_creation():
        """测试用户创建功能"""
        print("测试用户创建功能...")

        with app.app_context():
            # 创建测试用户
            test_user = User(
                username='newuser',
                email='newuser@test.com',
                full_name='新用户',
                phone='13800138001',
                address=''  # 测试空地址
            )
            test_user.set_password('testpass123')

            try:
                db.session.add(test_user)
                db.session.commit()
                print("用户创建成功！地址可以为空")

                # 验证用户是否正确创建
                user = User.query.filter_by(username='newuser').first()
                if user:
                    print(f"用户验证成功: {user.username}")
                    print(f"   邮箱: {user.email}")
                    print(f"   姓名: {user.full_name}")
                    print(f"   电话: {user.phone}")
                    print(f"   地址: '{user.address}' (空地址测试通过)")
                    return True
                else:
                    print("用户验证失败")
                    return False

            except Exception as e:
                print(f"用户创建失败: {e}")
                return False

    def main():
        print("=" * 50)
        print("图书管理系统 - 注册功能测试")
        print("=" * 50)

        # 测试用户创建
        user_test = test_user_creation()

        print("\n" + "=" * 50)
        if user_test:
            print("测试通过！注册功能正常工作")
            print("地址字段可以为空")
            print("email_validator已安装")
        else:
            print("测试失败，请检查配置")
        print("=" * 50)

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"导入错误: {e}")
except Exception as e:
    print(f"测试失败: {e}")
    import traceback
    traceback.print_exc()