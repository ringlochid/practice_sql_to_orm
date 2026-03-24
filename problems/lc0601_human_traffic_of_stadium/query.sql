WITH valid_number AS (
    SELECT
        *
    FROM
        Stadium
    WHERE
        people >= 100
),
cons_rows AS(
    SELECT
        s3.id AS id1,
        s2.id AS id2,
        s1.id AS id3
    FROM
        valid_number s1
        JOIN valid_number s2 ON s1.id - 1 = s2.id
        JOIN valid_number s3 ON s2.id - 1 = s3.id
)
SELECT
    *
FROM
    Stadium
WHERE
    id IN (
        SELECT
            id1
        FROM
            cons_rows
        UNION
        SELECT
            id2
        FROM
            cons_rows
        UNION
        SELECT
            id3
        FROM
            cons_rows
    )