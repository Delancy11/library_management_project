#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql

# Connect to database
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    database='library_management',
    charset='utf8mb4'
)

try:
    cursor = connection.cursor()

    print("=== 管理员表检查 ===")
    cursor.execute("SELECT id, username, email FROM admins")
    admins = cursor.fetchall()

    if not admins:
        print("管理员表中没有记录")
    else:
        for admin in admins:
            print(f"管理员: ID {admin[0]} - {admin[1]} ({admin[2]})")

    print("\n=== 普通用户表检查 ===")
    cursor.execute("SELECT id, username, email FROM users")
    users = cursor.fetchall()

    if not users:
        print("用户表中没有记录")
    else:
        for user in users:
            print(f"普通用户: ID {user[0]} - {user[1]} ({user[2]})")

    print("\n=== 权限验证 ===")
    print("系统权限设计:")
    print("- admins表中的用户是管理员")
    print("- users表中的用户是普通用户")
    print("- user1应该只存在于users表中，是普通用户")
    print("- admin应该只存在于admins表中，是管理员")

    cursor.close()
    connection.close()

except Exception as e:
    print(f"检查失败: {e}")
    connection.close()