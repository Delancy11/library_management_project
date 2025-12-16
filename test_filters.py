#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试快速筛选功能
"""

from run import create_app
from models import db, BorrowRecord
from datetime import datetime, timedelta

def test_filters():
    app = create_app()

    with app.app_context():
        print("检查借阅记录筛选功能...")

        # 检查今日到期
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        today_due = BorrowRecord.query.filter(
            BorrowRecord.status == 'borrowed',
            BorrowRecord.due_date >= today_start,
            BorrowRecord.due_date < today_end
        ).count()

        print(f"✓ 今日到期记录数: {today_due}")

        # 检查本周到期
        now = datetime.utcnow()
        days_since_monday = now.weekday()
        week_start = (now - timedelta(days=days_since_monday)).replace(hour=0, minute=0, second=0, microsecond=0)
        week_end = week_start + timedelta(days=7)

        week_due = BorrowRecord.query.filter(
            BorrowRecord.status == 'borrowed',
            BorrowRecord.due_date >= week_start,
            BorrowRecord.due_date < week_end
        ).count()

        print(f"✓ 本周到期记录数: {week_due}")

        # 检查逾期记录
        overdue = BorrowRecord.query.filter(
            BorrowRecord.status == 'borrowed',
            BorrowRecord.due_date < datetime.utcnow()
        ).count()

        print(f"✓ 逾期记录数: {overdue}")

        # 检查活跃用户（30天内）
        start_date = datetime.utcnow() - timedelta(days=30)
        active_users = BorrowRecord.query.filter(
            BorrowRecord.borrow_date >= start_date
        ).count()

        print(f"✓ 30天内借阅记录数: {active_users}")

        # 检查长期逾期（90天以上）
        long_overdue_start = datetime.utcnow() - timedelta(days=90)
        long_overdue = BorrowRecord.query.filter(
            BorrowRecord.status == 'borrowed',
            BorrowRecord.due_date < long_overdue_start
        ).count()

        print(f"✓ 长期逾期记录数(>90天): {long_overdue}")

        print("\n筛选功能测试完成！")

if __name__ == '__main__':
    test_filters()