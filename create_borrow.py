#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql
from datetime import datetime, timedelta

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

    # Get testuser user
    cursor.execute("SELECT id, username FROM users WHERE username = 'testuser'")
    user = cursor.fetchone()
    if not user:
        print("没有找到testuser用户，使用mary用户")
        cursor.execute("SELECT id, username FROM users WHERE username = 'mary'")
        user = cursor.fetchone()

    # Get first available book
    cursor.execute("SELECT id, title, available_quantity FROM books WHERE available_quantity > 0 LIMIT 1")
    book = cursor.fetchone()

    print(f"用户: {user[1]} (ID: {user[0]})")
    print(f"图书: {book[1]} (ID: {book[0]}, 可借: {book[2]})")

    if user and book:
        # Create borrow record
        borrow_date = datetime.now()
        due_date = borrow_date + timedelta(days=30)

        # Insert borrow record
        cursor.execute("""
            INSERT INTO borrow_records (user_id, book_id, borrow_date, due_date, status, created_at)
            VALUES (%s, %s, %s, %s, 'borrowed', %s)
        """, (user[0], book[0], borrow_date, due_date, borrow_date))

        # Update book available quantity
        cursor.execute("UPDATE books SET available_quantity = available_quantity - 1 WHERE id = %s", (book[0],))

        connection.commit()

        print("成功创建借阅记录！")
        print(f"借阅日期: {borrow_date.strftime('%Y-%m-%d %H:%M')}")
        print(f"应还日期: {due_date.strftime('%Y-%m-%d %H:%M')}")

        # Verify the record
        cursor.execute("""
            SELECT br.id, u.username, b.title
            FROM borrow_records br
            JOIN users u ON br.user_id = u.id
            JOIN books b ON br.book_id = b.id
            WHERE br.user_id = %s AND br.status = 'borrowed'
        """, (user[0],))
        records = cursor.fetchall()
        print(f"\n该用户当前有 {len(records)} 个活跃借阅记录")

    cursor.close()
    connection.close()
    print("\n操作完成！请刷新用户仪表板页面。")

except Exception as e:
    print(f"错误: {e}")
    connection.close()