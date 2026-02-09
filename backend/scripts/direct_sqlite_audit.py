
import sqlite3
import os

def direct_audit():
    db_path = 'db.sqlite3'
    if not os.path.exists(db_path):
        print(f"Error: {db_path} not found.")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    with open('scripts/direct_audit_results.txt', 'w', encoding='utf-8') as f:
        f.write("--- DIRECT SQLITE AUDIT ---\n\n")
        
        # 1. Topics with 'Pozitif'
        f.write("Topics containing 'Pozitif':\n")
        cur.execute("SELECT id, month, week, \"order\", title FROM coaching_topic WHERE title LIKE '%Pozitif%'")
        for row in cur.fetchall():
            f.write(f"ID: {row[0]} | M: {row[1]} | W: {row[2]} | Ord: {row[3]} | Title: {row[4]}\n")
            
        # 2. Student 10 Progress
        f.write("\nStudent 10 Progress Status:\n")
        cur.execute("SELECT topic_id, is_completed FROM coaching_studentprogress WHERE student_id = 10")
        for row in cur.fetchall():
            f.write(f"TopicID: {row[0]} | Completed: {row[1]}\n")
            
        # 3. Subject Names
        f.write("\nSubjects:\n")
        cur.execute("SELECT id, name FROM coaching_subject")
        for row in cur.fetchall():
            f.write(f"ID: {row[0]} | Name: {repr(row[1])}\n")

        # 4. Student 10 Config
        f.write("\nStudent 10 Config:\n")
        cur.execute("SELECT current_academic_month, current_academic_week FROM coaching_coachingconfig WHERE student_id = 10")
        for row in cur.fetchall():
            f.write(f"Month: {row[0]} | Week: {row[1]}\n")

    conn.close()
    print("Direct audit complete. Results in scripts/direct_audit_results.txt")

if __name__ == "__main__":
    direct_audit()
