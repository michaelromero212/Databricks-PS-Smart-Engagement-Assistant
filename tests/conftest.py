"""
Pytest fixtures for testing
"""
import pytest
import sqlite3
import os
import tempfile
import shutil


@pytest.fixture(scope="session")
def test_db_path():
    """Create a test database path"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_engagement.db")
        yield db_path


@pytest.fixture(scope="function")
def test_db(test_db_path):
    """Create a test database with sample data"""
    conn = sqlite3.connect(test_db_path)
    cursor = conn.cursor()
    
    # Create tables
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
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS slack_messages (
            message_id TEXT PRIMARY KEY,
            project_id TEXT,
            user_id TEXT,
            timestamp TEXT,
            content TEXT,
            thread_id TEXT,
            channel_name TEXT,
            is_bot BOOLEAN
        )
    ''')
    
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
            story_points INTEGER
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meetings (
            meeting_id TEXT PRIMARY KEY,
            project_id TEXT,
            date TEXT,
            title TEXT,
            attendees TEXT,
            agenda TEXT,
            notes TEXT
        )
    ''')
    
    # Insert sample data
    cursor.execute('''
        INSERT INTO projects VALUES 
        ('PROJ-TEST', 'Test Corp', 'Test Project', '2024-01-01', '2024-12-31', 100000, 'Active')
    ''')
    
    cursor.execute('''
        INSERT INTO slack_messages VALUES 
        ('MSG-001', 'PROJ-TEST', 'user1', '2024-11-01 10:00:00', 'Test message 1', NULL, 'general', 0),
        ('MSG-002', 'PROJ-TEST', 'user2', '2024-11-02 11:00:00', 'Test message 2', NULL, 'general', 0)
    ''')
    
    cursor.execute('''
        INSERT INTO jira_tickets VALUES 
        ('TICKET-001', 'PROJ-TEST', 'Test ticket 1', 'Description 1', 'Done', 'High', '2024-01-01', '2024-01-05', 'Alice', 5),
        ('TICKET-002', 'PROJ-TEST', 'Test ticket 2', 'Description 2', 'Open', 'Critical', '2024-01-02', '2024-01-02', 'Bob', 3)
    ''')
    
    cursor.execute('''
        INSERT INTO meetings VALUES 
        ('MEET-001', 'PROJ-TEST', '2024-11-15', 'Weekly Sync', 'Alice, Bob', 'Status update', 'Good progress')
    ''')
    
    conn.commit()
    conn.close()
    
    yield test_db_path
    
    # Cleanup
    if os.path.exists(test_db_path):
        os.remove(test_db_path)


@pytest.fixture
def sample_project():
    """Sample project data"""
    return {
        "project_id": "PROJ-SAMPLE",
        "client_name": "Sample Corp",
        "project_name": "Sample Project",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "budget": 150000,
        "status": "Active"
    }
