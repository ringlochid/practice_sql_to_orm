WITH valid_number AS (
    SELECT
        id,
        visit_date,
        people
    FROM
        Stadium
    WHERE
        people >= 100
),
grouped_rows AS (
    SELECT
        id,
        visit_date,
        people,
        id - ROW_NUMBER() OVER (
            ORDER BY
                id
        ) AS group_id
    FROM
        valid_number
),
valid_group AS (
    SELECT
        group_id
    FROM
        grouped_rows
    GROUP BY
        group_id
    HAVING
        COUNT(*) >= 3
)
SELECT
    id,
    visit_date,
    people
FROM
    grouped_rows
WHERE
    group_id IN (
        SELECT
            group_id
        FROM
            valid_group
    )
ORDER BY
    visit_date