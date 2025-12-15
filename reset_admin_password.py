#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重置管理员密码脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Admin

def reset_admin_password():
    """重置管理员密码"""
    with app.app_context():
        try:
            # 查找管理员
            admin = Admin.query.filter_by(username='admin').first()

            if admin:
                # 重置密码
                admin.set_password('admin123')
                db.session.commit()
                print("管理员密码重置成功！")
                print("用户名: admin")
                print("密码: admin123")
            else:
                # 创建新管理员
                admin = Admin(
                    username='admin',
                    email='admin@library.com'
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("管理员账户创建成功！")
                print("用户名: admin")
                print("密码: admin123")

        except Exception as e:
            print(f"操作失败: {e}")
            db.session.rollback()

if __name__ == '__main__':
    reset_admin_password()