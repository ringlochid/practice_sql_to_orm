-- Write your PostgreSQL query statement below
WITH valid_trips AS (
    SELECT
        *
    FROM
        Trips t
        JOIN Users c ON t.client_id = c.users_id
        AND c.banned = 'No'
        JOIN Users d ON t.driver_id = d.users_id
        AND d.banned = 'No'
    WHERE
        t.request_at BETWEEN '2013-10-01'
        AND '2013-10-03'
),
aggregated AS (
    SELECT
        request_at,
        COUNT(*) AS total_requests,
        SUM(
            CASE
                WHEN status IN ('cancelled_by_driver', 'cancelled_by_client') THEN 1
                ELSE 0
            END
        ) AS cancelled_requests
    FROM
        valid_trips
    GROUP BY
        request_at
)
SELECT
    request_at AS "Day",
    ROUND(cancelled_requests :: DECIMAL / total_requests, 2) AS "Cancellation Rate"
FROM
    aggregated;