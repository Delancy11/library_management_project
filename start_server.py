#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图书管理系统启动脚本 - 简化版
"""

import os
import sys
from flask import Flask
from create_database import create_database

def main():
    print("=" * 50)
    print("图书管理系统")
    print("=" * 50)

    # 创建数据库
    try:
        print("正在创建数据库...")
        create_database()
        print("数据库创建成功")
    except Exception as e:
        print(f"数据库创建失败: {e}")
        print("请确保MySQL服务正在运行，并且配置正确")
        sys.exit(1)

    # 导入应用
    try:
        print("正在初始化应用...")
        from app import app, initialize_database

        # 初始化数据库
        if not initialize_database():
            print("数据库初始化失败")
            sys.exit(1)

        print("应用初始化成功")
    except Exception as e:
        print(f"应用初始化失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # 启动信息
    print("\n" + "-" * 50)
    print("启动Web服务器...")
    print("访问地址: http://localhost:5000")
    print("管理员账户: admin / admin123")
    print("测试用户: testuser / test123")
    print("调试模式: 开启")
    print("按 Ctrl+C 停止服务器")
    print("-" * 50)

    # 启动服务器
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"服务器启动失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()