-- Lab 5 Part F: Analytical queries for the assistant database

-- F1: Requests per intent
SELECT intent, COUNT(*) AS requests
FROM interaction
GROUP BY intent
ORDER BY requests DESC;

-- F2: Average latency per intent (rounded to 1 decimal)
SELECT intent, ROUND(AVG(latency_ms), 1) AS avg_latency_ms
FROM interaction
GROUP BY intent
ORDER BY avg_latency_ms DESC;

-- F3: Topics with the most thumbs-down (negative feedback: rating = -1)
SELECT i.topic, COUNT(*) AS thumbs_down
FROM feedback f
JOIN interaction i ON f.request_id = i.request_id
WHERE f.rating = -1 AND i.topic IS NOT NULL
GROUP BY i.topic
ORDER BY thumbs_down DESC;

-- Homework H2: Status and percentage of degraded and resolved per intent
-- Analytic question: What are the status across all intent and percentage of degraded and resolved of each intent?
SELECT intent,
       MAX(latency_ms) AS worst_latency,
       MIN(latency_ms) AS best_latency,
       COUNT(id) AS total_requests,
       ROUND((SUM(CASE WHEN resolved THEN 1 ELSE 0 END) * 100.0) / COUNT(id), 2) AS resolve_pct,
       ROUND((SUM(CASE WHEN degraded THEN 1 ELSE 0 END) * 100.0) / COUNT(id), 2) AS degraded_pct
FROM interaction
GROUP BY intent
ORDER BY total_requests DESC;
