# Databricks notebook source
# MAGIC %md
# MAGIC # PS Engagement Data Ingestion
# MAGIC 
# MAGIC This notebook demonstrates production data ingestion patterns for the PS Smart Engagement Assistant.
# MAGIC 
# MAGIC **Key Features:**
# MAGIC - Delta Lake bronze tables
# MAGIC - Incremental loading
# MAGIC - Data quality checks
# MAGIC - Schema enforcement

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from delta.tables import *

# Initialize paths
bronze_path = "/mnt/ps_analytics/bronze/"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Sample: Ingest Slack Messages

# COMMAND ----------

# Simulate Slack API data (in production, this would be actual API calls)
slack_data = spark.createDataFrame([
    ("msg_001", "2024-01-15 09:30:00", "user_123", "channel_ps", 
     "Client is asking about the Q4 deliverables timeline", "question", 3.2),
    ("msg_002", "2024-01-15 10:15:00", "user_456", "channel_ps",
     "I've updated the project roadmap document", "update", 4.5),
    ("msg_003", "2024-01-15 11:00:00", "user_789", "channel_support",
     "Urgent: Production issue with client dashboard", "escalation", 1.8),
], ["message_id", "timestamp", "user_id", "channel", "text", "message_type", "sentiment_score"])

# Write to Delta Lake with merge logic
slack_data.write \
    .format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .save(f"{bronze_path}/slack_messages")

print(f"✅ Ingested {slack_data.count()} Slack messages")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Data Quality Checks

# COMMAND ----------

from pyspark.sql.functions import col, count, when

# Load bronze data
bronze_slack = spark.read.format("delta").load(f"{bronze_path}/slack_messages")

# Quality checks
quality_report = bronze_slack.agg(
    count("*").alias("total_records"),
    count(when(col("text").isNull(), 1)).alias("null_text"),
    count(when(col("sentiment_score") < 0, 1)).alias("invalid_sentiment"),
    countDistinct("message_id").alias("unique_messages")
)

display(quality_report)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Next Steps
# MAGIC - Run `02_data_processing` notebook to clean and transform data
# MAGIC - Schedule this notebook to run hourly in production