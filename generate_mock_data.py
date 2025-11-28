import os
import sqlite3
import random
from datetime import datetime, timedelta
from src.data_gen.schema import init_db
from src.data_gen.slack_gen import generate_slack_data
from src.data_gen.jira_gen import generate_jira_data
from src.data_gen.meeting_gen import generate_meeting_data, generate_action_items

DB_PATH = "data/engagement.db"

PROJECTS = [
    {"id": "PROJ-ALPHA", "client": "Acme Corp", "name": "Cloud Migration"},
    {"id": "PROJ-BETA", "client": "Globex", "name": "Data Lake Implementation"},
    {"id": "PROJ-GAMMA", "client": "Soylent Corp", "name": "ML Ops Pipeline"},
    {"id": "PROJ-DELTA", "client": "Initech", "name": "Real-time Analytics"},
    {"id": "PROJ-EPSILON", "client": "Weyland-Yutani", "name": "ETL Modernization"},
    {"id": "PROJ-ZETA", "client": "Tyrell Corp", "name": "Streaming Platform"},
    {"id": "PROJ-ETA", "client": "Cyberdyne", "name": "Feature Store Implementation"},
    {"id": "PROJ-THETA", "client": "Massive Dynamic", "name": "Data Governance"},
    {"id": "PROJ-IOTA", "client": "Umbrella Corp", "name": "Unity Catalog Rollout"},
    {"id": "PROJ-KAPPA", "client": "Buy N Large", "name": "Lakehouse Migration"},
    {"id": "PROJ-LAMBDA", "client": "OCP", "name": "Workflow Orchestration"},
    {"id": "PROJ-MU", "client": "Stark Industries", "name": "Serverless Analytics"}
]

def populate_db():
    # Initialize DB
    init_db(DB_PATH)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print(f"Generating data for {len(PROJECTS)} projects...")
    
    for proj in PROJECTS:
        # 1. Insert Project
        cursor.execute('''
            INSERT OR REPLACE INTO projects (project_id, client_name, project_name, start_date, end_date, budget, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            proj["id"], 
            proj["client"], 
            proj["name"], 
            (datetime.now() - timedelta(days=60)).isoformat(),
            (datetime.now() + timedelta(days=60)).isoformat(),
            random.randint(50000, 200000),
            "Active"
        ))
        
        # 2. Generate & Insert Slack Messages (100 → 300)
        messages = generate_slack_data(proj["id"], num_messages=300)
        for msg in messages:
            cursor.execute('''
                INSERT INTO slack_messages (message_id, project_id, user_id, timestamp, content, thread_id, channel_name, is_bot)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                msg["message_id"], msg["project_id"], msg["user_id"], msg["timestamp"], 
                msg["content"], msg["thread_id"], msg["channel_name"], msg["is_bot"]
            ))
            
        # 3. Generate & Insert Jira Tickets (30 → 75)
        tickets = generate_jira_data(proj["id"], num_tickets=75)
        for ticket in tickets:
            cursor.execute('''
                INSERT INTO jira_tickets (ticket_id, project_id, summary, description, status, priority, created_at, updated_at, assignee, story_points)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                ticket["ticket_id"], ticket["project_id"], ticket["summary"], ticket["description"],
                ticket["status"], ticket["priority"], ticket["created_at"], ticket["updated_at"],
                ticket["assignee"], ticket["story_points"]
            ))
            
        # 4. Generate & Insert Meetings and Action Items (10 → 20)
        meetings = generate_meeting_data(proj["id"], num_meetings=20)
        for meeting in meetings:
            cursor.execute('''
                INSERT INTO meetings (meeting_id, project_id, date, title, attendees, agenda, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                meeting["meeting_id"], meeting["project_id"], meeting["date"], meeting["title"],
                meeting["attendees"], meeting["agenda"], meeting["notes"]
            ))
            
            # Action Items for Meeting
            actions = generate_action_items(meeting["meeting_id"], "meeting")
            for action in actions:
                cursor.execute('''
                    INSERT INTO action_items (item_id, source_id, source_type, description, owner, due_date, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    action["item_id"], action["source_id"], action["source_type"], 
                    action["description"], action["owner"], action["due_date"], action["status"]
                ))
                
    conn.commit()
    conn.close()
    print("Data generation complete!")

if __name__ == "__main__":
    populate_db()
