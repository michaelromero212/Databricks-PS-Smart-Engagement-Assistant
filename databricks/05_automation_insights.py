# Databricks notebook source
# MAGIC %md
# MAGIC # Automation Opportunity Detection
# MAGIC 
# MAGIC Identifies repetitive patterns and suggests automation opportunities

# COMMAND ----------

from pyspark.sql import functions as F

# COMMAND ----------

# Load clustered messages
messages_df = spark.read.format("delta").load("/mnt/ps_analytics/silver/slack_messages")
clusters_df = spark.read.format("delta").load("/mnt/ps_analytics/ml_features/message_clusters")

# Join datasets
enriched_df = messages_df.join(clusters_df, "message_id")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Identify High-Frequency Patterns

# COMMAND ----------

# Find clusters with high frequency (potential automation candidates)
automation_candidates = enriched_df \
    .groupBy("cluster") \
    .agg(
        F.count("*").alias("frequency"),
        F.avg("sentiment_score").alias("avg_sentiment"),
        F.collect_list("text").alias("sample_texts")
    ) \
    .filter(F.col("frequency") > 10) \
    .withColumn("sample_text", F.col("sample_texts")[0]) \
    .withColumn("estimated_hours_monthly", F.col("frequency") * 0.25) \
    .withColumn("priority", 
        F.when(F.col("frequency") > 50, "High")
         .when(F.col("frequency") > 20, "Medium")
         .otherwise("Low")
    ) \
    .select("cluster", "frequency", "avg_sentiment", "sample_text", 
            "estimated_hours_monthly", "priority") \
    .orderBy(F.desc("frequency"))

display(automation_candidates)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Generate Recommendations

# COMMAND ----------

recommendations = automation_candidates \
    .withColumn("recommendation",
        F.when(F.col("sample_text").contains("report"), "Automate: Create self-service reporting dashboard")
         .when(F.col("sample_text").contains("status"), "Automate: Weekly status digest email")
         .when(F.col("sample_text").contains("documentation"), "Automate: Generate documentation from Jira tickets")
         .otherwise("Automate: Create FAQ bot for common questions")
    )

display(recommendations.select("cluster", "frequency", "recommendation", "estimated_hours_monthly"))

# COMMAND ----------

# Save recommendations
recommendations.write \
    .format("delta") \
    .mode("overwrite") \
    .save("/mnt/ps_analytics/gold/automation_opportunities")

print("✅ Automation opportunities saved!")