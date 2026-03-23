WITH bidirectional_friends AS (
    SELECT user1_id AS user_id, user2_id AS friend_id
    FROM Friendship
    UNION ALL
    SELECT user2_id AS user_id, user1_id AS friend_id
    FROM Friendship
)
SELECT bf.user_id, page_id, count(*) AS friends_likes
FROM bidirectional_friends bf
JOIN Likes l ON bf.friend_id = l.user_id
WHERE (bf.user_id, l.page_id) NOT IN(
    SELECT bf.user_id, l.page_id
    FROM bidirectional_friends bf
    JOIN Likes l
    ON bf.user_id = l.user_id
)
GROUP BY bf.user_id, l.page_id
