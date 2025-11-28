import pandas as pd
import sqlite3

DB_PATH = "data/engagement.db"

def detect_opportunities():
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query("SELECT * FROM analysis_results", conn)
    except Exception:
        print("Analysis results not found. Run analysis pipeline first.")
        conn.close()
        return []
    
    opportunities = []
    
    # 1. High Frequency Topics
    topic_counts = df['topic'].value_counts()
    for topic, count in topic_counts.items():
        if count > 3 and topic != "General Inquiry":
            opportunities.append({
                "type": "Pattern",
                "title": f"Frequent {topic} Requests",
                "description": f"Detected {count} requests related to {topic} this month.",
                "impact": "High" if count > 10 else "Medium",
                "estimated_savings": f"{count * 0.5} hours/month"
            })
            
    # 2. Cluster-based Insights
    # If a cluster is tight (low variance) and has many points, it's a specific recurring issue
    # For prototype, we just look at cluster sizes
    cluster_counts = df['cluster'].value_counts()
    for cluster_id, count in cluster_counts.items():
        if count > 5:
            opportunities.append({
                "type": "Cluster",
                "title": f"Recurring Issue Cluster #{cluster_id}",
                "description": f"A group of {count} similar messages was identified.",
                "impact": "High",
                "estimated_savings": f"{count * 1.0} hours/month"
            })
            
    # 3. Sentiment-based (Escalation Prevention)
    neg_sentiment = df[df['sentiment'] == 'NEGATIVE']
    if len(neg_sentiment) > 0:
         opportunities.append({
                "type": "Risk",
                "title": "Negative Sentiment Spike",
                "description": f"Detected {len(neg_sentiment)} negative interactions.",
                "impact": "Critical",
                "estimated_savings": "N/A (Client Satisfaction)"
            })

    conn.close()
    return opportunities

if __name__ == "__main__":
    ops = detect_opportunities()
    for op in ops:
        print(op)
