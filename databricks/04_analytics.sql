-- Databricks notebook source
-- MAGIC %md
-- MAGIC # PS Engagement Analytics - SQL Dashboard Queries
-- MAGIC 
-- MAGIC This notebook contains enterprise-grade SQL queries for analyzing Professional Services engagement data.

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

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Project Health Dashboard

-- COMMAND ----------

WITH project_metrics AS (
  SELECT 
    p.project_id,
    p.client_name,
    p.project_name,
    p.status,
    p.budget,
    COUNT(DISTINCT j.ticket_id) as total_tickets,
    SUM(CASE WHEN j.status = 'Done' THEN 1 ELSE 0 END) as completed_tickets,
    AVG(s.sentiment_score) as avg_sentiment,
    COUNT(DISTINCT m.meeting_id) as total_meetings,
    SUM(CASE WHEN a.status = 'Completed' THEN 1 ELSE 0 END) as completed_actions,
    COUNT(DISTINCT a.item_id) as total_actions
  FROM delta.`/mnt/ps_analytics/projects` p
  LEFT JOIN delta.`/mnt/ps_analytics/jira_tickets` j ON p.project_id = j.project_id
  LEFT JOIN delta.`/mnt/ps_analytics/slack_messages` s ON p.project_id = s.project_id
  LEFT JOIN delta.`/mnt/ps_analytics/meetings` m ON p.project_id = m.project_id
  LEFT JOIN delta.`/mnt/ps_analytics/action_items` a ON m.meeting_id = a.source_id
  GROUP BY p.project_id, p.client_name, p.project_name, p.status, p.budget
)
SELECT 
  project_id,
  client_name,
  project_name,
  status,
  budget,
  total_tickets,
  ROUND(completed_tickets * 100.0 / NULLIF(total_tickets, 0), 1) as completion_percentage,
  ROUND(avg_sentiment, 2) as avg_sentiment,
  CASE 
    WHEN avg_sentiment >= 0.7 THEN '😊 Positive'
    WHEN avg_sentiment >= 0.4 THEN '😐 Neutral'
    ELSE '😟 Needs Attention'
  END as sentiment_status,
  total_meetings,
  ROUND(completed_actions * 100.0 / NULLIF(total_actions, 0), 1) as action_completion_rate,
  CASE 
    WHEN completed_tickets * 100.0 / NULLIF(total_tickets, 0) >= 80 
      AND avg_sentiment >= 0.6 THEN 'On Track'
    WHEN completed_tickets * 100.0 / NULLIF(total_tickets, 0) >= 60 THEN 'At Risk'
    ELSE 'Critical'
  END as health_status
FROM project_metrics
ORDER BY 
  CASE health_status 
    WHEN 'Critical' THEN 1 
    WHEN 'At Risk' THEN 2 
    ELSE 3 
  END,
  avg_sentiment ASC;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Team Utilization \u0026 Capacity Analysis

-- COMMAND ----------

WITH team_workload AS (
  SELECT 
    assignee,
    COUNT(DISTINCT project_id) as active_projects,
    COUNT(*) as total_tickets,
    SUM(story_points) as total_story_points,
    SUM(CASE WHEN status IN ('In Progress', 'Review') THEN 1 ELSE 0 END) as in_progress_count,
    SUM(CASE WHEN priority = 'Critical' THEN 1 ELSE 0 END) as critical_items,
    AVG(CASE WHEN status = 'Done' 
      THEN datediff(updated_at, created_at) 
      ELSE NULL END) as avg_completion_days
  FROM delta.`/mnt/ps_analytics/jira_tickets`
  WHERE assignee IS NOT NULL
  GROUP BY assignee
),
capacity_calc AS (
  SELECT 
    assignee,
    active_projects,
    total_tickets,
    total_story_points,
    in_progress_count,
    critical_items,
    ROUND(avg_completion_days, 1) as avg_completion_days,
    ROUND(total_story_points / 13.0, 1) as workload_weeks,
    CASE 
      WHEN total_story_points > 80 THEN 'Over Capacity'
      WHEN total_story_points > 50 THEN 'At Capacity'
      ELSE 'Under Capacity'
    END as capacity_status
  FROM team_workload
)
SELECT 
  assignee,
  active_projects,
  total_tickets,
  total_story_points,
  in_progress_count,
  critical_items,
  avg_completion_days,
  workload_weeks,
  capacity_status,
  CASE 
    WHEN capacity_status = 'Over Capacity' THEN '🔴 High Risk'
    WHEN capacity_status = 'At Capacity' THEN '🟡 Monitor'
    ELSE '🟢 Healthy'
  END as risk_indicator
FROM capacity_calc
ORDER BY total_story_points DESC;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Client Sentiment Trend Analysis

-- COMMAND ----------

WITH weekly_sentiment AS (
  SELECT 
    s.project_id,
    p.client_name,
    DATE_TRUNC('week', s.timestamp) as week_start,
    AVG(s.sentiment_score) as avg_sentiment,
    COUNT(*) as message_count,
    SUM(CASE WHEN s.sentiment_score < 0.3 THEN 1 ELSE 0 END) as negative_count
  FROM delta.`/mnt/ps_analytics/slack_messages` s
  JOIN delta.`/mnt/ps_analytics/projects` p ON s.project_id = p.project_id
  WHERE s.timestamp >= date_sub(current_date(), 90)
  GROUP BY s.project_id, p.client_name, DATE_TRUNC('week', s.timestamp)
),
sentiment_change AS (
  SELECT 
    project_id,
    client_name,
    week_start,
    avg_sentiment,
    message_count,
    negative_count,
    LAG(avg_sentiment, 1) OVER (PARTITION BY project_id ORDER BY week_start) as prev_week_sentiment,
    ROUND(avg_sentiment - LAG(avg_sentiment, 1) OVER (PARTITION BY project_id ORDER BY week_start), 3) as sentiment_change
  FROM weekly_sentiment
)
SELECT 
  client_name,
  week_start,
  ROUND(avg_sentiment, 2) as avg_sentiment,
  message_count,
  negative_count,
  ROUND(prev_week_sentiment, 2) as prev_week_sentiment,
  sentiment_change,
  CASE 
    WHEN sentiment_change > 0.1 THEN '📈 Improving'
    WHEN sentiment_change < -0.1 THEN '📉 Declining'
    ELSE '➡️ Stable'
  END as trend,
  CASE 
    WHEN sentiment_change < -0.15 AND avg_sentiment < 0.5 THEN 'ALERT: Escalate to Manager'
    WHEN negative_count > message_count * 0.3 THEN 'WARNING: High Negative Volume'
    ELSE 'OK'
  END as action_required
FROM sentiment_change
WHERE week_start >= date_sub(current_date(), 30)
ORDER BY week_start DESC, sentiment_change ASC;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## ROI \u0026 Automation Impact Calculator

-- COMMAND ----------

WITH automation_candidates AS (
  SELECT 
    c.cluster,
    COUNT(DISTINCT s.message_id) as occurrence_count,
    COUNT(DISTINCT s.project_id) as affected_projects,
    AVG(EXTRACT(HOUR FROM (s.thread_end - s.timestamp))) as avg_resolution_hours,
    PERCENTILE(EXTRACT(HOUR FROM (s.thread_end - s.timestamp)), 0.5) as median_resolution_hours
  FROM delta.`/mnt/ps_analytics/ml_features/message_clusters` c
  JOIN delta.`/mnt/ps_analytics/slack_messages` s ON c.message_id = s.message_id
  WHERE s.thread_end IS NOT NULL
  GROUP BY c.cluster
  HAVING COUNT(DISTINCT s.message_id) >= 10
),
roi_calculation AS (
  SELECT 
    cluster,
    occurrence_count,
    affected_projects,
    ROUND(avg_resolution_hours, 2) as avg_resolution_hours,
    ROUND(median_resolution_hours, 2) as median_resolution_hours,
    ROUND(occurrence_count * avg_resolution_hours * 0.7, 1) as potential_hours_saved,
    ROUND(occurrence_count * avg_resolution_hours * 0.7 * 150, 0) as potential_cost_savings,
    CASE 
      WHEN occurrence_count >= 50 AND avg_resolution_hours >= 2 THEN 1
      WHEN occurrence_count >= 30 AND avg_resolution_hours >= 1 THEN 2
      WHEN occurrence_count >= 15 THEN 3
      ELSE 4
    END as priority_rank
  FROM automation_candidates
)
SELECT 
  cluster,
  occurrence_count,
  affected_projects,
  avg_resolution_hours,
  median_resolution_hours,
  potential_hours_saved,
  potential_cost_savings as potential_annual_savings_usd,
  CASE priority_rank
    WHEN 1 THEN 'P1 - Immediate'
    WHEN 2 THEN 'P2 - High'
    WHEN 3 THEN 'P3 - Medium'
    ELSE 'P4 - Low'
  END as automation_priority,
  CASE 
    WHEN potential_cost_savings >= 50000 THEN 'Executive Approval Required'
    WHEN potential_cost_savings >= 20000 THEN 'Manager Approval Required'
    ELSE 'Team Decision'
  END as approval_level
FROM roi_calculation
ORDER BY priority_rank ASC, potential_cost_savings DESC;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Response Time SLA Compliance

-- COMMAND ----------

WITH response_times AS (
  SELECT 
    p.project_id,
    p.client_name,
    j.ticket_id,
    j.priority,
    j.created_at,
    j.updated_at,
    EXTRACT(HOUR FROM (j.updated_at - j.created_at)) as response_hours,
    CASE j.priority
      WHEN 'Critical' THEN 4
      WHEN 'High' THEN 24
      WHEN 'Medium' THEN 48
      ELSE 72
    END as sla_hours
  FROM delta.`/mnt/ps_analytics/jira_tickets` j
  JOIN delta.`/mnt/ps_analytics/projects` p ON j.project_id = p.project_id
  WHERE j.created_at >= date_sub(current_date(), 30)
),
sla_compliance AS (
  SELECT 
    project_id,
    client_name,
    priority,
    COUNT(*) as total_tickets,
    SUM(CASE WHEN response_hours <= sla_hours THEN 1 ELSE 0 END) as within_sla,
    ROUND(AVG(response_hours), 1) as avg_response_hours,
    sla_hours
  FROM response_times
  GROUP BY project_id, client_name, priority, sla_hours
)
SELECT 
  client_name,
  priority,
  total_tickets,
  within_sla,
  ROUND(within_sla * 100.0 / total_tickets, 1) as sla_compliance_pct,
  avg_response_hours,
  sla_hours,
  CASE 
    WHEN within_sla * 100.0 / total_tickets >= 95 THEN '✅ Excellent'
    WHEN within_sla * 100.0 / total_tickets >= 85 THEN '✔️ Good'
    WHEN within_sla * 100.0 / total_tickets >= 75 THEN '⚠️ Needs Improvement'
    ELSE '❌ Below Target'
  END as performance_rating
FROM sla_compliance
ORDER BY client_name, 
  CASE priority 
    WHEN 'Critical' THEN 1 
    WHEN 'High' THEN 2 
    WHEN 'Medium' THEN 3 
    ELSE 4 
  END;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Topic Distribution \u0026 Knowledge Gaps

-- COMMAND ----------

WITH topic_analysis AS (
  SELECT 
    topic,
    COUNT(DISTINCT message_id) as message_count,
    COUNT(DISTINCT project_id) as project_count,
    AVG(sentiment_score) as avg_sentiment,
    SUM(CASE WHEN contains(content, '?') THEN 1 ELSE 0 END) as question_count
  FROM delta.`/mnt/ps_analytics/silver/slack_messages`
  WHERE timestamp >= date_sub(current_date(), 60)
  GROUP BY topic
),
ranked_topics AS (
  SELECT 
    topic,
    message_count,
    project_count,
    ROUND(avg_sentiment, 2) as avg_sentiment,
    question_count,
    ROUND(question_count * 100.0 / message_count, 1) as question_rate_pct,
    RANK() OVER (ORDER BY message_count DESC) as volume_rank
  FROM topic_analysis
)
SELECT 
  topic,
  message_count,
  project_count,
  avg_sentiment,
  question_count,
  question_rate_pct,
  CASE 
    WHEN question_rate_pct > 50 THEN '📚 Documentation Opportunity'
    WHEN avg_sentiment < 0.4 AND message_count > 20 THEN '⚡ Training Opportunity'
    WHEN message_count > 100 THEN '🤖 Automation Candidate'
    ELSE '✅ Manageable'
  END as recommendation,
  CASE 
    WHEN volume_rank <= 5 THEN 'Core Competency'
    WHEN volume_rank <= 15 THEN 'Secondary Focus'
    ELSE 'Emerging Topic'
  END as strategic_importance
FROM ranked_topics
ORDER BY message_count DESC
LIMIT 20;