# Databricks notebook source
# MAGIC %md
# MAGIC # Delta Lake Integration - PS Engagement Data
# MAGIC 
# MAGIC This notebook demonstrates how to convert the SQLite engagement data into Delta Lake format for production-scale analytics.
# MAGIC 
# MAGIC **Benefits of Delta Lake:**
# MAGIC - ACID transactions for data reliability
# MAGIC - Time travel for audit trails
# MAGIC - Schema enforcement and evolution
# MAGIC - Optimized file management with Z-ordering
# MAGIC - Unified batch and streaming

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Setup and Configuration

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
from delta.tables import DeltaTable

# Initialize Spark session (already initialized in Databricks)
spark = SparkSession.builder.getOrCreate()

# Define Delta Lake paths
DELTA_BASE_PATH = "/mnt/ps_analytics"
PROJECTS_TABLE = f"{DELTA_BASE_PATH}/projects"
SLACK_TABLE = f"{DELTA_BASE_PATH}/slack_messages"
JIRA_TABLE = f"{DELTA_BASE_PATH}/jira_tickets"
MEETINGS_TABLE = f"{DELTA_BASE_PATH}/meetings"
ANALYSIS_TABLE = f"{DELTA_BASE_PATH}/analysis_results"

print("✅ Configuration complete")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Define Schemas

# COMMAND ----------

# Projects schema
projects_schema = StructType([
    StructField("project_id", StringType(), False),
    StructField("client_name", StringType(), False),
    StructField("project_name", StringType(), False),
    StructField("start_date", TimestampType(), True),
    StructField("end_date", TimestampType(), True),
    StructField("budget", IntegerType(), True),
    StructField("status", StringType(), True)
])

# Slack messages schema
slack_schema = StructType([
    StructField("message_id", StringType(), False),
    StructField("project_id", StringType(), False),
    StructField("user_id", StringType(), True),
    StructField("timestamp", TimestampType(), False),
    StructField("content", StringType(), True),
    StructField("thread_id", StringType(), True),
    StructField("channel_name", StringType(), True),
    StructField("is_bot", BooleanType(), True)
])

# Jira tickets schema
jira_schema = StructType([
    StructField("ticket_id", StringType(), False),
    StructField("project_id", StringType(), False),
    StructField("summary", StringType(), True),
    StructField("description", StringType(), True),
    StructField("status", StringType(), True),
    StructField("priority", StringType(), True),
    StructField("created_at", TimestampType(), True),
    StructField("updated_at", TimestampType(), True),
    StructField("assignee", StringType(), True),
    StructField("story_points", IntegerType(), True)
])

print("✅ Schemas defined")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Load Data from CSV/JSON (Mock Upload)
# MAGIC 
# MAGIC **In Production:** This would read from DBFS upload or external source (S3, ADLS, GCS)

# COMMAND ----------

# EXAMPLE: Load projects from uploaded CSV
# df_projects = spark.read.format("csv").option("header", "true").schema(projects_schema).load("/FileStore/tables/projects.csv")

# For demo purposes, create sample data
df_projects_sample = spark.createDataFrame([
    ("PROJ-ALPHA", "Acme Corp", "Cloud Migration", "2024-10-01", "2025-01-01", 150000, "Active"),
    ("PROJ-BETA", "Globex", "Data Lake Implementation", "2024-09-15", "2024-12-31", 200000, "Active"),
], ["project_id", "client_name", "project_name", "start_date", "end_date", "budget", "status"])

df_projects = df_projects_sample.withColumn("start_date", to_timestamp(col("start_date"))) \
                                 .withColumn("end_date", to_timestamp(col("end_date")))

display(df_projects)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Write to Delta Lake

# COMMAND ----------

# Write projects to Delta Lake
df_projects.write.format("delta").mode("overwrite").save(PROJECTS_TABLE)

print(f"✅ Projects written to Delta table: {PROJECTS_TABLE}")

# Create Delta table metadata
spark.sql(f"""
CREATE TABLE IF NOT EXISTS delta_ps.projects
USING DELTA
LOCATION '{PROJECTS_TABLE}'
COMMENT 'Professional Services engagement projects'
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Demonstrate Delta Lake Features

# COMMAND ----------

# MAGIC %md
# MAGIC ### 5.1 Time Travel

# COMMAND ----------

# Query current version
current_df = spark.read.format("delta").load(PROJECTS_TABLE)
print(f"Current row count: {current_df.count()}")

# View table history
delta_table = DeltaTable.forPath(spark, PROJECTS_TABLE)
display(delta_table.history())

# Query previous version (if exists)
# versioned_df = spark.read.format("delta").option("versionAsOf", 0).load(PROJECTS_TABLE)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 5.2 Upsert (Merge) Operation

# COMMAND ----------

# Create new data to merge
new_projects = spark.createDataFrame([
    ("PROJ-GAMMA", "Soylent Corp", "ML Ops Pipeline", "2024-11-01", "2025-02-28", 180000, "Active"),
    ("PROJ-ALPHA", "Acme Corp", "Cloud Migration", "2024-10-01", "2025-01-01", 175000, "Active"),  # Updated budget
], ["project_id", "client_name", "project_name", "start_date", "end_date", "budget", "status"])

new_projects = new_projects.withColumn("start_date", to_timestamp(col("start_date"))) \
                            .withColumn("end_date", to_timestamp(col("end_date")))

# Perform merge
delta_table.alias("target").merge(
    new_projects.alias("source"),
    "target.project_id = source.project_id"
).whenMatchedUpdateAll() \
 .whenNotMatchedInsertAll() \
 .execute()

print("✅ Merge complete")
display(spark.read.format("delta").load(PROJECTS_TABLE))

# COMMAND ----------

# MAGIC %md
# MAGIC ### 5.3 Optimize and Z-Order

# COMMAND ----------

# Optimize table for faster queries
spark.sql(f"OPTIMIZE delta.`{PROJECTS_TABLE}` ZORDER BY (project_id, status)")

print("✅ Table optimized with Z-ordering")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Create Views for Analysis

# COMMAND ----------

# Create a view for active projects
spark.sql(f"""
CREATE OR REPLACE VIEW delta_ps.active_projects AS
SELECT 
    project_id,
    client_name,
    project_name,
    budget,
    DATEDIFF(end_date, CURRENT_DATE()) as days_remaining
FROM delta.`{PROJECTS_TABLE}`
WHERE status = 'Active'
""")

display(spark.sql("SELECT * FROM delta_ps.active_projects"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Next Steps
# MAGIC 
# MAGIC **Production Deployment:**
# MAGIC 1. Upload actual SQLite export (CSV/Parquet) to DBFS
# MAGIC 2. Create Delta tables for all entities (Slack, Jira, Meetings)
# MAGIC 3. Set up incremental ingestion pipeline
# MAGIC 4. Configure Unity Catalog for governance
# MAGIC 5. Create Databricks SQL dashboards
# MAGIC 6. Schedule workflow jobs for daily refresh
