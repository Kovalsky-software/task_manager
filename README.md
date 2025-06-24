# Database Task Manager

`main.py` is a standalone Python command-line tool designed to manage chapters and tasks stored in a SQLite database (`db_file.db`). It complements a Kivy-based application where users can only view tasks, providing administrative control to add, delete, or rename chapters and tasks outside the main GUI. Tasks are stored as JSON arrays within the `chapters` table, enabling flexible and scalable data management.

## Features

- **List Tasks**: Displays all chapters and their associated tasks in a clear, organized format.
- **Add Chapters**: Creates one or more chapters using semicolon-separated input (e.g., `Chapter 1;Chapter 2`).
- **Delete Chapters**: Removes one or more chapters, with a confirmation prompt if a chapter contains tasks to prevent accidental data loss.
- **Rename Chapter**: Updates the name of a single chapter, ensuring no conflicts with existing names.
- **Add Tasks**: Adds one or more tasks to a specified chapter using semicolon-separated input (e.g., `Task 1.1;Task 1.2`).
- **Delete Tasks**: Removes one or more tasks from a chapter.
- **Rename Task**: Updates the name of a single task within a chapter.
- **Error Handling**: Prevents duplicate chapters or tasks and provides clear feedback for invalid inputs or database errors.
- **No External Dependencies**: Uses Python's built-in `sqlite3` and `json` modules.

## Usage

1. **Prerequisites**:
   - Python 3.x with `sqlite3` (included in standard library).
   - A SQLite database (`db_file.db`) with the schema: `chapters (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, tasks TEXT NOT NULL DEFAULT '[]')`.
2. **Initialize the Database**:
   - Create `db_file.db` using an SQL script (e.g., `init_db.sql`). Example initialization:

     ```python
     import sqlite3
     with open('init_db.sql', 'r', encoding='utf-8') as f:
         sql_script = f.read()
     conn = sqlite3.connect('db_file.db')
     cursor = conn.cursor()
     cursor.executescript(sql_script)
     conn.commit()
     conn.close()
     ```
3. **Run the Script**:
   - Save the script as `main.py`.
   - Execute: `python main.py`.
   - Follow the interactive menu to perform operations:

     ```
     Task Manager
     1. List all chapters and tasks
     2. Add chapters (separate by ;)
     3. Delete chapters (separate by ;)
     4. Rename a chapter
     5. Add tasks to a chapter (separate by ;)
     6. Delete tasks from a chapter (separate by ;)
     7. Rename a task
     8. Exit
     ```
4. **Example Operations**:
   - Add chapters: `Chapter 11;Chapter 12`
   - Delete chapters with tasks: Prompts for confirmation (e.g., `Chapter 1 contains 3 task(s). Are you sure? (y/n)`).
   - Add tasks: `Task 3.4;Task 3.5` to `Chapter 3`.
   - Delete tasks: `Task 3.1;Task 3.2` from `Chapter 3`.

## Notes

- **Compatibility**: Designed to work with a Kivy application that uses `db_file.db` for read-only task display. Changes made by this script are immediately reflected in the Kivy app’s task view.
- **Schema**: Expects a `chapters` table with `id`, `name`, and `tasks` (JSON array of task objects, e.g., `[{"name": "Task 1.1"}]`.
- **Case Sensitivity**: Chapter and task names are case-sensitive.
- **Semicolon-Separated Input**: Allows batch operations for adding/deleting chapters or tasks (e.g., `Chapter 1;Chapter 2`).
- **Safety**: Confirmation prompts protect against accidental deletion of chapters with tasks.

This tool provides a robust and user-friendly way to manage database content, ensuring flexibility for administrators while maintaining data integrity for the main application.нужно ли
