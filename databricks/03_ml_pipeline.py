# Databricks notebook source
# MAGIC %md
# MAGIC # ML Pipeline: Embeddings & Clustering at Scale

# COMMAND ----------

import mlflow
import mlflow.sklearn
from sentence_transformers import SentenceTransformer
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Set MLflow experiment
mlflow.set_experiment("/Users/your_email/ps_engagement_ml")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Load Data from Silver Layer

# COMMAND ----------

# Read silver data
silver_df = spark.read.format("delta").load("/mnt/ps_analytics/silver/slack_messages")

# Convert to pandas for embedding generation (in production, use pandas UDF for distributed processing)
texts_df = silver_df.select("message_id", "text").limit(1000).toPandas()

print(f"Processing {len(texts_df)} messages")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Generate Embeddings

# COMMAND ----------

with mlflow.start_run(run_name="embedding_generation"):
    # Log parameters
    mlflow.log_param("model", "all-MiniLM-L6-v2")
    mlflow.log_param("num_texts", len(texts_df))
    
    # Load model
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    # Generate embeddings
    embeddings = model.encode(texts_df['text'].tolist(), show_progress_bar=True)
    
    mlflow.log_metric("embedding_dimension", embeddings.shape[1])
    
    print(f"✅ Generated embeddings: {embeddings.shape}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Clustering Analysis

# COMMAND ----------

with mlflow.start_run(run_name="clustering_analysis"):
    # Parameters
    n_clusters = 5
    mlflow.log_param("n_clusters", n_clusters)
    mlflow.log_param("algorithm", "KMeans")
    
    # Fit model
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(embeddings)
    
    # Calculate metrics
    sil_score = silhouette_score(embeddings, clusters)
    mlflow.log_metric("silhouette_score", sil_score)
    mlflow.log_metric("inertia", kmeans.inertia_)
    
    # Log model
    mlflow.sklearn.log_model(kmeans, "kmeans_model")
    
    print(f"✅ Silhouette Score: {sil_score:.3f}")
    
    # Add clusters to dataframe
    texts_df['cluster'] = clusters

# COMMAND ----------

# MAGIC %md
# MAGIC ## Analyze Cluster Themes

# COMMAND ----------

# Show sample messages from each cluster
for i in range(n_clusters):
    print(f"\n{'='*60}")
    print(f"CLUSTER {i} - Sample Messages:")
    print(f"{'='*60}")
    cluster_samples = texts_df[texts_df['cluster'] == i]['text'].head(3)
    for idx, text in enumerate(cluster_samples, 1):
        print(f"{idx}. {text[:100]}...")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Save Results Back to Delta Lake

# COMMAND ----------

# Convert to Spark DataFrame and save
results_df = spark.createDataFrame(texts_df[['message_id', 'cluster']])

results_df.write \
    .format("delta") \
    .mode("overwrite") \
    .save("/mnt/ps_analytics/ml_features/message_clusters")

print("✅ Results saved to Delta Lake")