WITH event_points AS (
    SELECT
        employee_id,
        task_id,
        start_time AS ep,
        1 AS delta
    FROM
        Tasks
    UNION
    SELECT
        employee_id,
        task_id,
        end_time AS ep,
        -1 AS delta
    FROM
        Tasks
),
concurrent_tasks AS (
    SELECT
        employee_id,
        SUM(delta) OVER(
            PARTITION BY employee_id
            ORDER BY
                ep
        ) AS ct
    FROM
        event_points
),
max_concurrent AS (
    SELECT
        employee_id,
        MAX(ct) AS mx_ct
    FROM
        concurrent_tasks
    GROUP BY
        employee_id
),
mx_end_point AS (
    SELECT
        employee_id,
        task_id,
        start_time,
        end_time,
        MAX(end_time) OVER(
            PARTITION BY employee_id
            ORDER BY
                start_time ROWS BETWEEN UNBOUNDED PRECEDING
                AND 1 PRECEDING
        ) AS mx_end
    FROM
        Tasks
),
delta_tasks AS (
    SELECT
        employee_id,
        task_id,
        start_time,
        end_time,
        CASE
            WHEN start_time >= mx_end THEN 1
            ELSE 0
        END AS group_delta
    FROM
        mx_end_point
),
grouped_tasks AS (
    SELECT
        employee_id,
        task_id,
        start_time,
        end_time,
        SUM(group_delta) OVER(
            PARTITION BY employee_id
            ORDER BY
                start_time
        ) AS group_id
    FROM
        delta_tasks
),
minmax_groups AS (
    SELECT
        employee_id,
        MIN(start_time) AS mn_st,
        MAX(end_time) AS mx_end
    FROM
        grouped_tasks
    GROUP BY
        employee_id,
        group_id
),
total_durations AS (
    SELECT
        employee_id,
        SUM(
            EXTRACT(
                EPOCH
                FROM
                    (mx_end - mn_st)
            ) / 3600.0
        ) AS total_duration
    FROM
        minmax_groups
    GROUP BY
        employee_id
)
SELECT
    mc.employee_id,
    FLOOR(td.total_duration) AS total_task_hours,
    mc.mx_ct AS max_concurrent_tasks
FROM
    max_concurrent mc
    JOIN total_durations td ON mc.employee_id = td.employee_id