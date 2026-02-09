
import sqlite3
import os

db_path = "c:\\Users\\USER\\Desktop\\ismail proje\\lgs_dershane\\backend\\db.sqlite3"

def audit_users():
    print(f"Auditing DB: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\n--- AUTH USERS ---")
    cursor.execute("SELECT id, username, is_active FROM auth_user")
    for row in cursor.fetchall():
        print(f"ID: {row[0]} | Username: {row[1]} | Active: {row[2]}")
        
    print("\n--- STUDENTS ---")
    cursor.execute("SELECT id, full_name, user_id FROM students_student")
    for row in cursor.fetchall():
        print(f"ID: {row[0]} | Name: {row[1]} | UserID: {row[2]}")
        
    conn.close()

if __name__ == "__main__":
    audit_users()
