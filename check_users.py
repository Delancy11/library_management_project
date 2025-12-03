#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    database='library_management',
    charset='utf8mb4'
)

cursor = connection.cursor()
cursor.execute("SELECT id, username, full_name FROM users")
users = cursor.fetchall()

print("所有用户:")
for user in users:
    print(f"  ID {user[0]}: {user[1]} ({user[2]})")

# Check if testuser exists
cursor.execute("SELECT id, username FROM users WHERE username = 'testuser'")
testuser = cursor.fetchone()

if testuser:
    print(f"\ntestuser 存在: ID {testuser[0]}")
else:
    print("\ntestuser 不存在，正在创建...")
    cursor.execute("""
        INSERT INTO users (username, email, full_name, phone, address, password_hash, created_at)
        VALUES ('testuser', 'test@example.com', '测试用户', '13800138000', '测试地址', 'hashed_password', NOW())
    """)
    connection.commit()
    print("testuser 创建成功!")

cursor.close()
connection.close()