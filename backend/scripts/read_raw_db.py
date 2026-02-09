
import sqlite3
import os

db_path = "c:\\Users\\USER\\Desktop\\ismail proje\\lgs_dershane\\backend\\db.sqlite3"

def check_raw_db():
    print(f"Checking DB at {db_path}...")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check student 10 config
        cursor.execute("SELECT id, current_academic_month, current_academic_week FROM coaching_coachingconfig WHERE student_id = 10")
        row = cursor.fetchone()
        if row:
            print(f"Student 10 Config: ID {row[0]}, Month {row[1]}, Week {row[2]}")
        else:
            print("Student 10 Config NOT FOUND in coaching_coachingconfig")
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_raw_db()
