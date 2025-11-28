import sqlite3
import os

def init_db(db_path="data/engagement.db"):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Projects/Engagements Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        project_id TEXT PRIMARY KEY,
        client_name TEXT NOT NULL,
        project_name TEXT NOT NULL,
        start_date TEXT,
        end_date TEXT,
        budget REAL,
        status TEXT
    )
    ''')
    
    # 2. Slack Messages Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS slack_messages (
        message_id TEXT PRIMARY KEY,
        project_id TEXT,
        user_id TEXT,
        timestamp TEXT,
        content TEXT,
        thread_id TEXT,
        channel_name TEXT,
        is_bot BOOLEAN,
        FOREIGN KEY (project_id) REFERENCES projects(project_id)
    )
    ''')
    
    # 3. Jira Tickets Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS jira_tickets (
        ticket_id TEXT PRIMARY KEY,
        project_id TEXT,
        summary TEXT,
        description TEXT,
        status TEXT,
        priority TEXT,
        created_at TEXT,
        updated_at TEXT,
        assignee TEXT,
        story_points INTEGER,
        FOREIGN KEY (project_id) REFERENCES projects(project_id)
    )
    ''')
    
    # 4. Meeting Notes Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS meetings (
        meeting_id TEXT PRIMARY KEY,
        project_id TEXT,
        date TEXT,
        title TEXT,
        attendees TEXT,
        agenda TEXT,
        notes TEXT,
        FOREIGN KEY (project_id) REFERENCES projects(project_id)
    )
    ''')
    
    # 5. Action Items Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS action_items (
        item_id TEXT PRIMARY KEY,
        source_id TEXT, -- meeting_id or message_id
        source_type TEXT, -- 'meeting' or 'slack'
        description TEXT,
        owner TEXT,
        due_date TEXT,
        status TEXT
    )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {db_path}")

if __name__ == "__main__":
    init_db()
