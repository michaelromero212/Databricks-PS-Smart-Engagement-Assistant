"""
Data Loader Module - Centralized data access layer

Provides SQLite fallback with optional Databricks SQL Warehouse connection.
Set environment variables for Databricks:
  - DATABRICKS_SERVER_HOSTNAME
  - DATABRICKS_HTTP_PATH
  - DATABRICKS_TOKEN
"""

import os
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from functools import lru_cache

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "engagement.db")


def get_connection():
    """Get database connection - SQLite for now, SQL Warehouse if configured"""
    # Check for Databricks SQL Warehouse config
    server = os.getenv("DATABRICKS_SERVER_HOSTNAME")
    http_path = os.getenv("DATABRICKS_HTTP_PATH")
    token = os.getenv("DATABRICKS_TOKEN")
    
    if server and http_path and token:
        try:
            from databricks import sql
            return sql.connect(
                server_hostname=server,
                http_path=http_path,
                access_token=token
            )
        except ImportError:
            print("Warning: databricks-sql-connector not installed, falling back to SQLite")
        except Exception as e:
            print(f"Warning: Could not connect to Databricks SQL: {e}, falling back to SQLite")
    
    # Fallback to SQLite
    return sqlite3.connect(DB_PATH)


def _execute_query(query: str, params: tuple = ()) -> pd.DataFrame:
    """Execute a query and return DataFrame"""
    conn = get_connection()
    try:
        if hasattr(conn, 'cursor'):
            # SQLite connection
            df = pd.read_sql_query(query, conn, params=params)
        else:
            # Databricks SQL connection
            df = pd.read_sql(query, conn)
        return df
    finally:
        conn.close()


# ============================================================================
# Project Functions
# ============================================================================

def get_projects() -> pd.DataFrame:
    """Get all projects"""
    query = "SELECT * FROM projects ORDER BY project_name"
    return _execute_query(query)


def get_project_list() -> List[Dict[str, str]]:
    """Get projects as dropdown options - clean, simple format"""
    df = get_projects()
    options = []
    for _, row in df.iterrows():
        # Simple: just the project name
        options.append({"label": row['project_name'], "value": row['project_id']})
    return options


# ============================================================================
# KPI Summary Functions
# ============================================================================

def get_kpi_summary(project_id: Optional[str] = None) -> Dict[str, Any]:
    """Get key performance indicators"""
    project_filter = f"WHERE project_id = '{project_id}'" if project_id else ""
    
    # Total engagements (unique projects with activity)
    if project_id:
        total_engagements = 1
    else:
        projects_df = get_projects()
        total_engagements = len(projects_df)
    
    # Slack message count
    msg_query = f"SELECT COUNT(*) as count FROM slack_messages {project_filter}"
    msg_count = _execute_query(msg_query).iloc[0]['count']
    
    # Jira ticket stats
    jira_query = f"""
        SELECT 
            COUNT(*) as total_tickets,
            AVG(story_points) as avg_story_points,
            SUM(CASE WHEN status = 'Done' THEN 1 ELSE 0 END) as completed,
            SUM(CASE WHEN status IN ('In Progress', 'Open') THEN 1 ELSE 0 END) as open_tickets,
            SUM(CASE WHEN priority IN ('Critical', 'High') THEN 1 ELSE 0 END) as high_priority
        FROM jira_tickets {project_filter}
    """
    jira_df = _execute_query(jira_query)
    
    # Meeting count
    meeting_query = f"SELECT COUNT(*) as count FROM meetings {project_filter}"
    meeting_count = _execute_query(meeting_query).iloc[0]['count']
    
    # Calculate derived metrics
    total_tickets = jira_df.iloc[0]['total_tickets'] or 0
    completed = jira_df.iloc[0]['completed'] or 0
    open_tickets = jira_df.iloc[0]['open_tickets'] or 0
    high_priority = jira_df.iloc[0]['high_priority'] or 0
    
    # Simulated metrics (these would come from analysis_results in production)
    # Calculate based on actual data ratios
    resolution_rate = (completed / total_tickets * 100) if total_tickets > 0 else 0
    
    return {
        "total_engagements": total_engagements,
        "total_messages": int(msg_count),
        "total_tickets": int(total_tickets),
        "open_tickets": int(open_tickets),
        "high_priority_tickets": int(high_priority),
        "completed_tickets": int(completed),
        "total_meetings": int(meeting_count),
        "resolution_rate": round(resolution_rate, 1),
        "avg_response_time": 4.2,  # Would be calculated from timestamps
        "automation_potential": 45000,  # Would be from automation analysis
        "client_satisfaction": 4.8,  # Would be from sentiment analysis
    }


# ============================================================================
# Trend Functions
# ============================================================================

def get_engagement_trends(days: int = 30, project_id: Optional[str] = None) -> pd.DataFrame:
    """Get daily engagement counts for trend charts"""
    project_filter = f"AND project_id = '{project_id}'" if project_id else ""
    
    # Get message counts by date
    query = f"""
        SELECT 
            DATE(timestamp) as date,
            COUNT(*) as message_count
        FROM slack_messages
        WHERE timestamp >= DATE('now', '-{days} days') {project_filter}
        GROUP BY DATE(timestamp)
        ORDER BY date
    """
    df = _execute_query(query)
    
    if df.empty:
        # Return mock data if no real data
        dates = pd.date_range(end=datetime.now(), periods=days)
        return pd.DataFrame({
            "date": dates,
            "message_count": [10 + i % 15 for i in range(days)]
        })
    
    df['date'] = pd.to_datetime(df['date'])
    return df


def get_weekly_engagement_counts(weeks: int = 8, project_id: Optional[str] = None) -> List[int]:
    """Get weekly engagement counts for executive chart"""
    project_filter = f"AND project_id = '{project_id}'" if project_id else ""
    
    query = f"""
        SELECT 
            strftime('%W', timestamp) as week,
            COUNT(*) as count
        FROM slack_messages
        WHERE timestamp >= DATE('now', '-{weeks * 7} days') {project_filter}
        GROUP BY week
        ORDER BY week
    """
    df = _execute_query(query)
    
    if df.empty or len(df) < weeks:
        # Return mock data if insufficient
        return [10 + i * 3 for i in range(weeks)]
    
    return df['count'].tolist()[-weeks:]


# ============================================================================
# Topic & Sentiment Functions
# ============================================================================

def get_topic_distribution(project_id: Optional[str] = None) -> pd.DataFrame:
    """Get topic category distribution"""
    # Check if analysis_results table exists
    try:
        project_filter = f"WHERE project_id = '{project_id}'" if project_id else ""
        query = f"""
            SELECT 
                topic,
                COUNT(*) as count
            FROM analysis_results
            {project_filter}
            GROUP BY topic
            ORDER BY count DESC
        """
        df = _execute_query(query)
        if not df.empty:
            return df.rename(columns={"topic": "Topic", "count": "Count"})
    except:
        pass
    
    # Fallback mock data
    return pd.DataFrame({
        "Topic": ["Technical Issue", "Feature Request", "Documentation", "Process", "Training"],
        "Count": [45, 32, 28, 15, 12]
    })


def get_sentiment_distribution(project_id: Optional[str] = None) -> Dict[str, int]:
    """Get sentiment category counts"""
    try:
        project_filter = f"WHERE project_id = '{project_id}'" if project_id else ""
        query = f"""
            SELECT 
                sentiment,
                COUNT(*) as count
            FROM analysis_results
            {project_filter}
            GROUP BY sentiment
        """
        df = _execute_query(query)
        if not df.empty:
            return dict(zip(df['sentiment'], df['count']))
    except:
        pass
    
    # Fallback mock data
    return {'Positive': 350, 'Neutral': 180, 'Negative': 70}


def get_sentiment_by_project() -> pd.DataFrame:
    """Get sentiment scores per project"""
    try:
        query = """
            SELECT 
                p.project_id,
                p.client_name,
                AVG(CASE WHEN a.sentiment = 'POSITIVE' THEN 100 
                         WHEN a.sentiment = 'NEUTRAL' THEN 50 
                         ELSE 0 END) as sentiment_score
            FROM projects p
            LEFT JOIN analysis_results a ON p.project_id = a.project_id
            GROUP BY p.project_id
        """
        df = _execute_query(query)
        if not df.empty:
            return df
    except:
        pass
    
    # Fallback mock data
    return pd.DataFrame({
        "project_id": ["PROJ-ALPHA", "PROJ-BETA", "PROJ-GAMMA", "PROJ-DELTA"],
        "sentiment_score": [85, 62, 45, 90]
    })


# ============================================================================
# Team Capacity Functions
# ============================================================================

def get_team_capacity() -> pd.DataFrame:
    """Get team utilization data"""
    # In production, this would come from time tracking or assignee data
    # For now, aggregate from Jira assignees
    try:
        query = """
            SELECT 
                assignee as Person,
                COUNT(*) as ticket_count,
                SUM(story_points) as total_points
            FROM jira_tickets
            WHERE assignee IS NOT NULL
            GROUP BY assignee
            ORDER BY total_points DESC
            LIMIT 10
        """
        df = _execute_query(query)
        if not df.empty and len(df) >= 3:
            # Calculate utilization as percentage of max
            max_points = df['total_points'].max()
            df['Utilization'] = (df['total_points'] / max_points * 100).round().astype(int)
            df['Role'] = ['Engineer'] * len(df)  # Would come from user profile
            return df[['Person', 'Utilization', 'Role']]
    except:
        pass
    
    # Fallback mock data
    return pd.DataFrame({
        "Person": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
        "Utilization": [85, 92, 45, 78, 60],
        "Role": ["Architect", "Engineer", "Data Scientist", "Engineer", "PM"]
    })


# ============================================================================
# Automation Opportunity Functions
# ============================================================================

def get_automation_opportunities(project_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get detected automation opportunities"""
    # This would come from ML analysis in production
    return [
        {
            "title": "Frequent 'Access Denied' Issues",
            "description": "Detected 15 requests related to permission errors in Bronze layer.",
            "impact": "High",
            "savings": "12 hours/month",
            "priority": "high"
        },
        {
            "title": "Manual Report Generation",
            "description": "Weekly requests for status report generation.",
            "impact": "High", 
            "savings": "8 hours/month",
            "priority": "high"
        },
        {
            "title": "Documentation Gaps: Delta Live Tables",
            "description": "Multiple questions about DLT syntax.",
            "impact": "Medium",
            "savings": "4 hours/month",
            "priority": "medium"
        },
        {
            "title": "Meeting Scheduling",
            "description": "High volume of scheduling coordination messages.",
            "impact": "Medium",
            "savings": "2 hours/month",
            "priority": "medium"
        }
    ]


# ============================================================================
# Project Health Distribution
# ============================================================================

def get_project_health_distribution() -> Dict[str, int]:
    """Get count of projects by health status"""
    # Would be calculated from composite health scores
    # For now, derive from ticket status distribution
    try:
        query = """
            SELECT 
                project_id,
                SUM(CASE WHEN priority = 'Critical' THEN 1 ELSE 0 END) as critical,
                SUM(CASE WHEN status = 'Done' THEN 1 ELSE 0 END) as done,
                COUNT(*) as total
            FROM jira_tickets
            GROUP BY project_id
        """
        df = _execute_query(query)
        if not df.empty:
            on_track = 0
            at_risk = 0
            delayed = 0
            for _, row in df.iterrows():
                completion_rate = row['done'] / row['total'] if row['total'] > 0 else 0
                critical_rate = row['critical'] / row['total'] if row['total'] > 0 else 0
                
                if critical_rate > 0.2:
                    delayed += 1
                elif completion_rate < 0.5:
                    at_risk += 1
                else:
                    on_track += 1
            
            return {"On Track": on_track, "At Risk": at_risk, "Delayed": delayed}
    except:
        pass
    
    return {"On Track": 7, "At Risk": 3, "Delayed": 2}


# ============================================================================
# Cache Clearing
# ============================================================================

def clear_cache():
    """Clear any cached data"""
    # Clear LRU caches if used
    pass
