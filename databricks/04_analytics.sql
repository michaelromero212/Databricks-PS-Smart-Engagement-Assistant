-- Databricks notebook source
-- MAGIC %md
-- MAGIC # PS Engagement Analytics - SQL Dashboard Queries

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Daily Engagement Trends

-- COMMAND ----------

SELECT 
  date,
  SUM(message_count) as total_messages,
  AVG(avg_sentiment) as overall_sentiment,
  SUM(urgent_count) as urgent_items,
  SUM(question_count) as questions
FROM delta.`/mnt/ps_analytics/gold/daily_metrics`
WHERE date >= date_sub(current_date(), 30)
GROUP BY date
ORDER BY date DESC;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Top Automation Opportunities

-- COMMAND ----------

WITH message_patterns AS (
  SELECT 
    cluster,
    COUNT(*) as frequency,
    AVG(sentiment_score) as avg_sentiment
  FROM delta.`/mnt/ps_analytics/silver/slack_messages` s
  JOIN delta.`/mnt/ps_analytics/ml_features/message_clusters` c
    ON s.message_id = c.message_id
  GROUP BY cluster
)
SELECT 
  cluster,
  frequency,
  ROUND(avg_sentiment, 2) as avg_sentiment,
  CASE 
    WHEN frequency > 50 THEN 'High Priority'
    WHEN frequency > 20 THEN 'Medium Priority'
    ELSE 'Low Priority'
  END as automation_priority,
  ROUND(frequency * 0.25, 1) as estimated_hours_saved_monthly
FROM message_patterns
ORDER BY frequency DESC;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Channel Performance Metrics

-- COMMAND ----------

SELECT 
  channel,
  message_type,
  COUNT(*) as message_count,
  ROUND(AVG(sentiment_score), 2) as avg_sentiment,
  SUM(CASE WHEN is_urgent THEN 1 ELSE 0 END) as urgent_count
FROM delta.`/mnt/ps_analytics/silver/slack_messages`
WHERE date >= date_sub(current_date(), 7)
GROUP BY channel, message_type
ORDER BY message_count DESC;