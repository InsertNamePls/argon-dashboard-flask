# migration_script.py
# Run this as a standalone script

import sqlite3
import os

def add_api_key_column():
    """Add api_key column to Users table"""
    try:
        # Get the current directory of the script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Try different potential paths for the database
        potential_paths = [
            'db.sqlite3',                         # Current directory
            'apps/db.sqlite3',                    # Relative to script
            os.path.join(current_dir, 'db.sqlite3'),  # Absolute in script dir
            os.path.join(current_dir, 'apps/db.sqlite3'),  # Script dir + apps
            os.path.join(current_dir, '../db.sqlite3'),  # One level up
            '/home/Ze/Documents/argon-dashboard-flask/apps/db.sqlite3'  # Absolute path
        ]
        
        # Try each path
        conn = None
        db_path = None
        
        for path in potential_paths:
            if os.path.exists(path):
                print(f"Found database at: {path}")
                db_path = path
                conn = sqlite3.connect(path)
                break
        
        if conn is None:
            print("Could not find the database file. Tried the following paths:")
            for path in potential_paths:
                print(f"- {path}")
            return False
            
        cursor = conn.cursor()
        
        # Check if column exists
        cursor.execute("PRAGMA table_info(Users)")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]
        
        if 'api_key' not in column_names:
            # Add the column
            cursor.execute('ALTER TABLE Users ADD COLUMN api_key TEXT;')
            print(f"Added api_key column to Users table in {db_path}")
        else:
            print("api_key column already exists")
        
        # Commit and close
        conn.commit()
        conn.close()
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = add_api_key_column()
    if success:
        print("Migration completed successfully")
    else:
        print("Migration failed")