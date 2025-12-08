#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动Flask应用
"""

import os
import sys

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app

    if __name__ == '__main__':
        print("=" * 50)
        print("图书管理系统 - 启动中...")
        print("=" * 50)
        print("访问地址: http://localhost:5000")
        print("管理员账户: admin / admin123")
        print("测试用户: testuser / test123")
        print("=" * 50)

        app.run(host='0.0.0.0', port=5000, debug=True)

except Exception as e:
    print(f"启动失败: {e}")
    import traceback
    traceback.print_exc()