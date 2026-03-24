WITH all_friendships AS (
    SELECT
        f.user_id AS user_id,
        f.friend_id AS friend_id
    FROM
        lc1892_page_recommendations_ii.friendships AS f
    UNION
    ALL
    SELECT
        f.friend_id AS user_id,
        f.user_id AS friend_id
    FROM
        lc1892_page_recommendations_ii.friendships AS f
)
SELECT
    af.user_id,
    l.page_id,
    COUNT(*) AS friends_likes
FROM
    all_friendships AS af
    JOIN lc1892_page_recommendations_ii.likes AS l ON af.friend_id = l.user_id
WHERE
    (af.user_id, l.page_id) NOT IN (
        SELECT
            user_id,
            page_id
        FROM
            lc1892_page_recommendations_ii.likes
    )
GROUP BY
    af.user_id,
    l.page_id
ORDER BY
    af.user_id,
    l.page_id;