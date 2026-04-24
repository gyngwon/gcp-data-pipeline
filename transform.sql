-- Table 1: Aggregated performance by country
CREATE OR REPLACE TABLE `your-gcp-project-id.your_dataset.country_performance` AS
SELECT
    country,
    COUNT(*) AS total_players,
    AVG(CAST(rank AS INT64)) AS avg_rank
FROM `your-gcp-projecxt-id.your_dataset.raw_cricket`
GROUP BY country;

-- Table 2: Top 10 players only
CREATE OR REPLACE TABLE `your-gcp-project-id.your_dataset.top_players` AS
SELECT
    name,
    country,
    CAST(rank AS INT64) AS rank
FROM `your-gcp-project-id.your_dataset.raw_cricket`
WHERE CAST(rank AS INT64) <= 10;

-- Table 3: Rank distribution groups
CREATE OR REPLACE TABLE `your-gcp-project-id.your_dataset.rank_distribution` AS
SELECT
    CASE
        WHEN CAST(rank AS INT64) <= 5  THEN 'Top 5'
        WHEN CAST(rank AS INT64) <= 10 THEN 'Top 10'
        ELSE 'Others'
    END AS rank_group,
    COUNT(*) AS count
FROM `your-gcp-project-id.your_dataset.raw_cricket`
GROUP BY rank_group;
