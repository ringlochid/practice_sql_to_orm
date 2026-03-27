WITH distinct_listens AS (
    SELECT DISTINCT
        l.user_id,
        l.song_id,
        l.day
    FROM
        lc1919_leetcodify_similar_friends.listens AS l
),
similar_friend_days AS (
    SELECT
        f.user1_id,
        f.user2_id,
        l1.day
    FROM
        lc1919_leetcodify_similar_friends.friendships AS f
        JOIN distinct_listens AS l1 ON l1.user_id = f.user1_id
        JOIN distinct_listens AS l2 ON l2.user_id = f.user2_id
        AND l2.song_id = l1.song_id
        AND l2.day = l1.day
    GROUP BY
        f.user1_id,
        f.user2_id,
        l1.day
    HAVING
        COUNT(*) >= 3
)
SELECT DISTINCT
    sfd.user1_id,
    sfd.user2_id
FROM
    similar_friend_days AS sfd
ORDER BY
    sfd.user1_id,
    sfd.user2_id;
