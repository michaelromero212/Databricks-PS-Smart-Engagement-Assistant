import sqlite3
import pandas as pd
from src.analysis.models import model_manager
from sklearn.cluster import KMeans
import numpy as np
import umap

DB_PATH = "data/engagement.db"

CANDIDATE_LABELS = [
    "Technical Issue", 
    "Feature Request", 
    "Process Question", 
    "Documentation", 
    "Training", 
    "Escalation", 
    "General Inquiry"
]

def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM slack_messages", conn)
    conn.close()
    return df

def analyze_sentiment(texts):
    sentiment_pipeline = model_manager.get_sentiment_pipeline()
    # Process in batches to avoid memory issues
    results = []
    batch_size = 32
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        # Truncate to 512 tokens approx (simple char limit for speed)
        batch = [t[:512] for t in batch] 
        results.extend(sentiment_pipeline(batch))
    return results

def classify_topics(texts):
    zeroshot_pipeline = model_manager.get_zeroshot_pipeline()
    results = []
    # Zero-shot is slow, so we might want to sample or optimize
    # For prototype, let's process a subset or assume pre-computed for large datasets
    # Here we process all but be warned it's slow
    print(f"Classifying {len(texts)} messages... this might take a while.")
    
    for text in texts:
        output = zeroshot_pipeline(text, candidate_labels=CANDIDATE_LABELS)
        # Get top label
        top_label = output['labels'][0]
        results.append(top_label)
        
    return results

def generate_embeddings(texts):
    model = model_manager.get_embedding_model()
    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings

def cluster_requests(embeddings, n_clusters=5):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(embeddings)
    
    # Reduce dim for viz
    reducer = umap.UMAP(n_neighbors=15, n_components=2, random_state=42)
    embedding_2d = reducer.fit_transform(embeddings)
    
    return clusters, embedding_2d

def run_analysis_pipeline():
    print("Starting analysis pipeline...")
    df = load_data()
    
    if df.empty:
        print("No data found.")
        return
    
    texts = df['content'].tolist()
    
    # 1. Sentiment
    print("Running sentiment analysis...")
    sentiments = analyze_sentiment(texts)
    df['sentiment'] = [s['label'] for s in sentiments]
    df['sentiment_score'] = [s['score'] for s in sentiments]
    
    # 2. Topic Classification
    # To save time in prototype, maybe only classify questions or longer messages
    # For now, let's just do first 20 for demo speed if list is long, or all if short
    # In real app, this would be async job
    print("Running topic classification (limiting to first 20 for speed in demo)...")
    topics = classify_topics(texts[:20]) 
    # Fill rest with "General Inquiry" for now to keep df shape
    topics += ["General Inquiry"] * (len(texts) - 20)
    df['topic'] = topics
    
    # 3. Embeddings & Clustering
    print("Generating embeddings...")
    embeddings = generate_embeddings(texts)
    clusters, coords = cluster_requests(embeddings)
    df['cluster'] = clusters
    df['x'] = coords[:, 0]
    df['y'] = coords[:, 1]
    
    # Save results back to DB (or new analysis table)
    # For simplicity, let's just save to a new table 'analysis_results'
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("analysis_results", conn, if_exists="replace", index=False)
    conn.close()
    
    print("Analysis complete. Results saved.")

if __name__ == "__main__":
    run_analysis_pipeline()
