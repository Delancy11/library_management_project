#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

def main():
    print("Starting Library Management System...")

    # Add current directory to path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    try:
        # Import and start Flask app
        from app import app
        from models import db

        with app.app_context():
            db.create_all()
            print("Database initialized successfully")

        print("Server starting at http://localhost:5000")
        print("Admin: admin / admin123")
        print("User: testuser / test123")
        print("Press Ctrl+C to stop")

        app.run(host='0.0.0.0', port=5000, debug=True)

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0

if __name__ == '__main__':
    main()