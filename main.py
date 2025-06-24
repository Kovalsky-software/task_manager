import sqlite3
import json

# Database file path
DB_FILE = 'db_file.db'

def connect_db():
    """Connect to the SQLite database and return connection and cursor."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        return conn, cursor
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None, None

def ensure_table_exists(cursor):
    """Ensure the chapters table exists."""
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chapters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                tasks TEXT NOT NULL DEFAULT '[]'
            )
        """)
    except Exception as e:
        print(f"Error creating table: {e}")

def add_chapter(conn, cursor, chapter_names):
    """Add one or more chapters."""
    try:
        chapters = chapter_names.split(';') if chapter_names else []
        if not chapters:
            print("Chapter names cannot be empty.")
            return
        for chapter_name in chapters:
            chapter_name = chapter_name.strip()
            if not chapter_name:
                continue
            cursor.execute("SELECT id FROM chapters WHERE name = ?", (chapter_name,))
            if cursor.fetchone():
                print(f"Chapter '{chapter_name}' already exists.")
                continue
            cursor.execute(
                "INSERT INTO chapters (name, tasks) VALUES (?, ?)",
                (chapter_name, '[]')
            )
            print(f"Chapter '{chapter_name}' added successfully.")
        conn.commit()
    except Exception as e:
        print(f"Error adding chapters: {e}")
        conn.rollback()

def delete_chapter(conn, cursor, chapter_names):
    """Delete one or more chapters with confirmation if they contain tasks."""
    try:
        chapters = chapter_names.split(';') if chapter_names else []
        if not chapters:
            print("Chapter names cannot be empty.")
            return
        for chapter_name in chapters:
            chapter_name = chapter_name.strip()
            if not chapter_name:
                continue
            cursor.execute("SELECT id, tasks FROM chapters WHERE name = ?", (chapter_name,))
            result = cursor.fetchone()
            if not result:
                print(f"Chapter '{chapter_name}' not found.")
                continue
            chapter_id, tasks_json = result
            tasks = json.loads(tasks_json)
            if tasks:
                confirm = input(f"Chapter '{chapter_name}' contains {len(tasks)} task(s). Are you sure you want to delete it? (y/n): ").strip().lower()
                if confirm != 'y':
                    print(f"Deletion of chapter '{chapter_name}' canceled.")
                    continue
            cursor.execute("DELETE FROM chapters WHERE id = ?", (chapter_id,))
            print(f"Chapter '{chapter_name}' deleted successfully.")
        conn.commit()
    except Exception as e:
        print(f"Error deleting chapters: {e}")
        conn.rollback()

def rename_chapter(conn, cursor, old_name, new_name):
    """Rename a chapter."""
    try:
        cursor.execute("SELECT id FROM chapters WHERE name = ?", (old_name,))
        result = cursor.fetchone()
        if not result:
            print(f"Chapter '{old_name}' not found.")
            return
        cursor.execute("SELECT id FROM chapters WHERE name = ?", (new_name,))
        if cursor.fetchone():
            print(f"Chapter '{new_name}' already exists.")
            return
        cursor.execute(
            "UPDATE chapters SET name = ? WHERE id = ?",
            (new_name, result[0])
        )
        conn.commit()
        print(f"Chapter '{old_name}' renamed to '{new_name}' successfully.")
    except Exception as e:
        print(f"Error renaming chapter: {e}")
        conn.rollback()

def add_task(conn, cursor, chapter_name, task_names):
    """Add one or more tasks to a chapter."""
    try:
        task_list = task_names.split(';') if task_names else []
        if not task_list:
            print("Task names cannot be empty.")
            return
        cursor.execute("SELECT id, tasks FROM chapters WHERE name = ?", (chapter_name,))
        result = cursor.fetchone()
        if result:
            chapter_id, tasks_json = result
            tasks = json.loads(tasks_json)
        else:
            tasks = []
            cursor.execute(
                "INSERT INTO chapters (name, tasks) VALUES (?, ?)",
                (chapter_name, '[]')
            )
            cursor.execute("SELECT id FROM chapters WHERE name = ?", (chapter_name,))
            chapter_id = cursor.fetchone()[0]
        
        added = False
        for task_name in task_list:
            task_name = task_name.strip()
            if not task_name:
                continue
            if any(task['name'] == task_name for task in tasks):
                print(f"Task '{task_name}' already exists in chapter '{chapter_name}'.")
                continue
            tasks.append({'name': task_name})
            print(f"Task '{task_name}' added to chapter '{chapter_name}' successfully.")
            added = True
        if added:
            cursor.execute(
                "UPDATE chapters SET tasks = ? WHERE id = ?",
                (json.dumps(tasks), chapter_id)
            )
            conn.commit()
    except Exception as e:
        print(f"Error adding tasks: {e}")
        conn.rollback()

def delete_task(conn, cursor, chapter_name, task_names):
    """Delete one or more tasks from a chapter."""
    try:
        task_list = task_names.split(';') if task_names else []
        if not task_list:
            print("Task names cannot be empty.")
            return
        cursor.execute("SELECT id, tasks FROM chapters WHERE name = ?", (chapter_name,))
        result = cursor.fetchone()
        if not result:
            print(f"Chapter '{chapter_name}' not found.")
            return
        chapter_id, tasks_json = result
        tasks = json.loads(tasks_json)
        original_len = len(tasks)
        for task_name in task_list:
            task_name = task_name.strip()
            if not task_name:
                continue
            updated_tasks = [task for task in tasks if task['name'] != task_name]
            if len(updated_tasks) == len(tasks):
                print(f"Task '{task_name}' not found in chapter '{chapter_name}'.")
            else:
                tasks = updated_tasks
                print(f"Task '{task_name}' deleted from chapter '{chapter_name}' successfully.")
        if len(tasks) < original_len:
            cursor.execute(
                "UPDATE chapters SET tasks = ? WHERE id = ?",
                (json.dumps(tasks), chapter_id)
            )
            conn.commit()
    except Exception as e:
        print(f"Error deleting tasks: {e}")
        conn.rollback()

def rename_task(conn, cursor, chapter_name, old_task_name, new_task_name):
    """Rename a task in a chapter."""
    try:
        cursor.execute("SELECT id, tasks FROM chapters WHERE name = ?", (chapter_name,))
        result = cursor.fetchone()
        if not result:
            print(f"Chapter '{chapter_name}' not found.")
            return
        chapter_id, tasks_json = result
        tasks = json.loads(tasks_json)
        task_found = False
        for task in tasks:
            if task['name'] == old_task_name:
                task['name'] = new_task_name
                task_found = True
                break
        if not task_found:
            print(f"Task '{old_task_name}' not found in chapter '{chapter_name}'.")
            return
        if any(task['name'] == new_task_name for task in tasks if task['name'] != old_task_name):
            print(f"Task '{new_task_name}' already exists in chapter '{chapter_name}'.")
            return
        cursor.execute(
            "UPDATE chapters SET tasks = ? WHERE id = ?",
            (json.dumps(tasks), chapter_id)
        )
        conn.commit()
        print(f"Task '{old_task_name}' renamed to '{new_task_name}' in chapter '{chapter_name}' successfully.")
    except Exception as e:
        print(f"Error renaming task: {e}")
        conn.rollback()

def list_tasks(cursor):
    """List all chapters and their tasks."""
    try:
        cursor.execute("SELECT name, tasks FROM chapters ORDER BY name")
        rows = cursor.fetchall()
        if not rows:
            print("No chapters found in the database.")
            return
        for row in rows:
            chapter_name, tasks_json = row
            tasks = json.loads(tasks_json)
            print(f"\nChapter: {chapter_name}")
            if tasks:
                for task in tasks:
                    print(f"  - {task['name']}")
            else:
                print("  (No tasks)")
    except Exception as e:
        print(f"Error listing tasks: {e}")

def main():
    conn, cursor = connect_db()
    if not conn or not cursor:
        return

    ensure_table_exists(cursor)

    while True:
        print("\nTask Manager")
        print("1. List all chapters and tasks")
        print("2. Add chapters (separate by ;)")
        print("3. Delete chapters (separate by ;)")
        print("4. Rename a chapter")
        print("5. Add tasks to a chapter (separate by ;)")
        print("6. Delete tasks from a chapter (separate by ;)")
        print("7. Rename a task")
        print("8. Exit")
        choice = input("Enter your choice (1-8): ").strip()

        if choice == '1':
            list_tasks(cursor)
        elif choice == '2':
            chapter_names = input("Enter chapter names (e.g., Chapter 1;Chapter 2): ").strip()
            add_chapter(conn, cursor, chapter_names)
        elif choice == '3':
            chapter_names = input("Enter chapter names to delete (e.g., Chapter 1;Chapter 2): ").strip()
            delete_chapter(conn, cursor, chapter_names)
        elif choice == '4':
            old_name = input("Enter current chapter name (e.g., Chapter 1): ").strip()
            new_name = input("Enter new chapter name: ").strip()
            if old_name and new_name:
                rename_chapter(conn, cursor, old_name, new_name)
            else:
                print("Chapter names cannot be empty.")
        elif choice == '5':
            chapter_name = input("Enter chapter name (e.g., Chapter 1): ").strip()
            task_names = input("Enter task names (e.g., Task 1.1;Task 1.2): ").strip()
            if chapter_name and task_names:
                add_task(conn, cursor, chapter_name, task_names)
            else:
                print("Chapter name and task names cannot be empty.")
        elif choice == '6':
            chapter_name = input("Enter chapter name (e.g., Chapter 1): ").strip()
            task_names = input("Enter task names to delete (e.g., Task 1.1;Task 1.2): ").strip()
            if chapter_name and task_names:
                delete_task(conn, cursor, chapter_name, task_names)
            else:
                print("Chapter name and task names cannot be empty.")
        elif choice == '7':
            chapter_name = input("Enter chapter name (e.g., Chapter 1): ").strip()
            old_task_name = input("Enter current task name (e.g., Task 1.1): ").strip()
            new_task_name = input("Enter new task name: ").strip()
            if chapter_name and old_task_name and new_task_name:
                rename_task(conn, cursor, chapter_name, old_task_name, new_task_name)
            else:
                print("Chapter name and task names cannot be empty.")
        elif choice == '8':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, 6, 7, or 8.")

    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()