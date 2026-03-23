WITH bidirectional_friends AS (
    SELECT user1_id AS user_id, user2_id AS friend_id
    FROM friend_relation
    UNION ALL
    SELECT user2_id AS user_id, user1_id AS friend_id
    FROM friend_relation
)
SELECT bf.user_id, l.page_id, COUNT(*) AS friends_likes
FROM bidirectional_friends AS bf
JOIN likes AS l ON bf.friend_id = l.user_id
WHERE (bf.user_id, l.page_id) NOT IN (
    SELECT user_id, page_id
    FROM likes
)
GROUP BY bf.user_id, l.page_id
ORDER BY bf.user_id, l.page_id;
