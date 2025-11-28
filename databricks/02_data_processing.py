# Databricks notebook source
# MAGIC %md
# MAGIC # Data Processing: Bronze → Silver → Gold
# MAGIC 
# MAGIC Demonstrates medallion architecture for PS engagement data

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.window import Window

# COMMAND ----------

# MAGIC %md
# MAGIC ## Bronze → Silver: Data Cleaning

# COMMAND ----------

# Read bronze data
bronze_slack = spark.read.format("delta").load("/mnt/ps_analytics/bronze/slack_messages")

# Clean and enrich
silver_slack = bronze_slack \
    .filter(col("text").isNotNull()) \
    .withColumn("text_length", F.length("text")) \
    .withColumn("word_count", F.size(F.split("text", " "))) \
    .withColumn("has_question", F.col("text").contains("?")) \
    .withColumn("is_urgent", F.col("text").rlike("(?i)(urgent|asap|critical)")) \
    .withColumn("date", F.to_date("timestamp")) \
    .dropDuplicates(["message_id"])

# Write to silver layer
silver_slack.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .save("/mnt/ps_analytics/silver/slack_messages")

print(f"✅ Processed {silver_slack.count()} records to Silver layer")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Silver → Gold: Aggregated Metrics

# COMMAND ----------

# Calculate daily metrics
gold_daily_metrics = silver_slack \
    .groupBy("date", "channel", "message_type") \
    .agg(
        F.count("*").alias("message_count"),
        F.avg("sentiment_score").alias("avg_sentiment"),
        F.sum(F.when(F.col("is_urgent"), 1).otherwise(0)).alias("urgent_count"),
        F.sum(F.when(F.col("has_question"), 1).otherwise(0)).alias("question_count")
    ) \
    .orderBy("date", "channel")

# Write to gold layer
gold_daily_metrics.write \
    .format("delta") \
    .mode("overwrite") \
    .save("/mnt/ps_analytics/gold/daily_metrics")

display(gold_daily_metrics)