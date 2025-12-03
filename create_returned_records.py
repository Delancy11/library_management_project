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

    # Get testuser
    cursor.execute("SELECT id, username FROM users WHERE username = 'testuser'")
    user = cursor.fetchone()

    # Get a book
    cursor.execute("SELECT id, title FROM books LIMIT 1")
    book = cursor.fetchone()

    if user and book:
        print(f"为用户 {user[1]} 创建借阅记录...")

        # Create returned borrow record
        borrow_date = datetime.now() - timedelta(days=15)
        due_date = borrow_date + timedelta(days=30)
        return_date = borrow_date + timedelta(days=10)  # 提前归还

        cursor.execute("""
            INSERT INTO borrow_records (user_id, book_id, borrow_date, due_date, return_date, status, created_at)
            VALUES (%s, %s, %s, %s, %s, 'returned', %s)
        """, (user[0], book[0], borrow_date, due_date, return_date, borrow_date))

        # Create another returned record
        borrow_date2 = datetime.now() - timedelta(days=30)
        due_date2 = borrow_date2 + timedelta(days=30)
        return_date2 = borrow_date2 + timedelta(days=20)

        cursor.execute("""
            INSERT INTO borrow_records (user_id, book_id, borrow_date, due_date, return_date, status, created_at)
            VALUES (%s, %s, %s, %s, %s, 'returned', %s)
        """, (user[0], book[0], borrow_date2, due_date2, return_date2, borrow_date2))

        connection.commit()
        print("成功创建2个已归还的借阅记录！")

    # Verify records
    cursor.execute("""
        SELECT status, COUNT(*) FROM borrow_records
        WHERE user_id = %s
        GROUP BY status
    """, (user[0],))

    records = cursor.fetchall()
    print(f"\n用户 {user[1]} 的借阅统计:")
    for record in records:
        status_name = "借阅中" if record[0] == 'borrowed' else "已归还"
        print(f"  {status_name}: {record[1]} 条记录")

    cursor.close()
    connection.close()
    print("\n测试数据创建完成！")

except Exception as e:
    print(f"错误: {e}")
    connection.close()