WITH per_user AS (
    SELECT
        spend_date,
        user_id,
        CASE
            WHEN COUNT(DISTINCT platform) = 2 THEN 'both'
            ELSE MAX(platform)
        END AS platform,
        SUM(amount) AS amount
    FROM
        Spending
    GROUP BY
        spend_date,
        user_id
),
all_dates AS (
    SELECT
        DISTINCT spend_date
    FROM
        Spending
),
all_platforms AS (
    SELECT
        'mobile' AS platform
    UNION
    ALL
    SELECT
        'desktop'
    UNION
    ALL
    SELECT
        'both'
)
SELECT
    d.spend_date,
    p.platform,
    COALESCE(SUM(u.amount), 0) AS total_amount,
    COUNT(u.user_id) AS total_users
FROM
    all_dates d
    CROSS JOIN all_platforms p
    LEFT JOIN per_user u ON u.spend_date = d.spend_date
    AND u.platform = p.platform
GROUP BY
    d.spend_date,
    p.platform;