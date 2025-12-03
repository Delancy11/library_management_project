#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql
from datetime import datetime, timedelta

def check_borrow_records():
    print("=== 检查借阅记录 ===")

    try:
        # Connect to database
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='library_management',
            charset='utf8mb4'
        )

        cursor = connection.cursor()

        # Check users
        print("\n1. 用户列表:")
        cursor.execute("SELECT id, username, full_name FROM users")
        users = cursor.fetchall()
        for user in users:
            print(f"  ID {user[0]}: {user[1]} ({user[2]})")

        # Check books
        print("\n2. 图书列表:")
        cursor.execute("SELECT id, title, author, available_quantity FROM books")
        books = cursor.fetchall()
        for book in books:
            print(f"  ID {book[0]}: {book[1]} - {book[2]} (可借: {book[3]})")

        # Check borrow records
        print("\n3. 借阅记录:")
        cursor.execute("""
            SELECT br.id, u.username, b.title, br.borrow_date, br.due_date, br.return_date, br.status
            FROM borrow_records br
            JOIN users u ON br.user_id = u.id
            JOIN books b ON br.book_id = b.id
            ORDER BY br.borrow_date DESC
        """)
        records = cursor.fetchall()

        if not records:
            print("  没有借阅记录")
        else:
            for record in records:
                status = "已借阅" if record[6] == 'borrowed' else "已归还"
                print(f"  记录ID {record[0]}: {record[1]} 借阅了《{record[2]}》 - {status}")

        # Check user specific borrow records
        if users:
            user_id = users[0][0]  # First user
            print(f"\n4. 用户 {users[0][1]} 的借阅统计:")
            cursor.execute("""
                SELECT COUNT(*) FROM borrow_records
                WHERE user_id = %s AND status = 'borrowed'
            """, (user_id,))
            active_borrows = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*) FROM borrow_records
                WHERE user_id = %s AND status = 'borrowed'
                AND due_date < NOW()
            """, (user_id,))
            overdue_count = cursor.fetchone()[0]

            print(f"  当前借阅数量: {active_borrows}")
            print(f"  即将逾期数量: {overdue_count}")

        cursor.close()
        connection.close()
        print("\n检查完成！")
        return True

    except Exception as e:
        print(f"检查失败: {e}")
        return False

def create_test_borrow():
    print("\n=== 创建测试借阅记录 ===")

    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='library_management',
            charset='utf8mb4'
        )

        cursor = connection.cursor()

        # Get first user and first available book
        cursor.execute("SELECT id, username FROM users LIMIT 1")
        user = cursor.fetchone()
        if not user:
            print("没有找到用户")
            return False

        cursor.execute("SELECT id, title FROM books WHERE available_quantity > 0 LIMIT 1")
        book = cursor.fetchone()
        if not book:
            print("没有可借阅的图书")
            return False

        print(f"用户 {user[1]} (ID: {user[0]})")
        print(f"图书 {book[1]} (ID: {book[0]})")

        # Create borrow record
        borrow_date = datetime.now()
        due_date = borrow_date + timedelta(days=30)

        cursor.execute("""
            INSERT INTO borrow_records (user_id, book_id, borrow_date, due_date, status, created_at)
            VALUES (%s, %s, %s, %s, 'borrowed', %s)
        """, (user[0], book[0], borrow_date, due_date, borrow_date))

        # Update book available quantity
        cursor.execute("UPDATE books SET available_quantity = available_quantity - 1 WHERE id = %s", (book[0],))

        connection.commit()
        cursor.close()
        connection.close()

        print(f"成功创建借阅记录！")
        print(f"借阅日期: {borrow_date.strftime('%Y-%m-%d %H:%M')}")
        print(f"应还日期: {due_date.strftime('%Y-%m-%d %H:%M')}")
        return True

    except Exception as e:
        print(f"创建失败: {e}")
        return False

if __name__ == '__main__':
    if check_borrow_records():
        # 如果没有借阅记录，创建一个测试记录
        import pymysql
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='library_management',
            charset='utf8mb4'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM borrow_records WHERE status = 'borrowed'")
        count = cursor.fetchone()[0]
        cursor.close()
        connection.close()

        if count == 0:
            print("没有活跃借阅记录，正在创建测试记录...")
            create_test_borrow()
            print("\n请刷新用户仪表板页面查看更新！")
        else:
            print("发现活跃借阅记录，请检查用户仪表板页面")
    else:
        print("检查失败")