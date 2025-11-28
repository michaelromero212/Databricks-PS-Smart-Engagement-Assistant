import sqlite3
import pandas as pd
import random

DB_PATH = "data/engagement.db"

def mock_analysis():
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query("SELECT * FROM slack_messages", conn)
    except Exception:
        print("No slack messages found. Run generate_mock_data.py first.")
        conn.close()
        return

    # Mock ML results
    topics = ["Technical Issue", "Feature Request", "Process Question", "Documentation", "Training", "Escalation", "General Inquiry"]
    sentiments = ["POSITIVE", "NEGATIVE", "NEUTRAL"]
    
    df['sentiment'] = [random.choice(sentiments) for _ in range(len(df))]
    df['sentiment_score'] = [random.uniform(0.5, 0.99) for _ in range(len(df))]
    df['topic'] = [random.choice(topics) for _ in range(len(df))]
    df['cluster'] = [random.randint(0, 4) for _ in range(len(df))]
    df['x'] = [random.uniform(-10, 10) for _ in range(len(df))]
    df['y'] = [random.uniform(-10, 10) for _ in range(len(df))]
    
    df.to_sql("analysis_results", conn, if_exists="replace", index=False)
    conn.close()
    print("Mock analysis complete. Results saved.")

if __name__ == "__main__":
    mock_analysis()
