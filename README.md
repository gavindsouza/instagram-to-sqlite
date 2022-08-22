# instagram-to-sqlite

<!--

[![PyPI](https://img.shields.io/pypi/v/instagram-to-sqlite.svg)](https://pypi.org/project/instagram-to-sqlite/)
[![GitHub Actions]()]()
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/gavindsouza/instagram-to-sqlite/blob/master/LICENSE)

-->

Save data from a Instagram takeout to a SQLite database.


## Mise en Place

```bash
git clone https://github.com/gavindsouza/instagram-to-sqlite
pip install -e ./instagram-to-sqlite
```

> This tool only supports JSON data takeouts.

## Ricing the potatoes

    $ instagram-to-sqlite chats insta-chats.db ~/Downloads/takeout-20190530.zip

This will create a database file called `insta-chats.db` if one does not already exist.


## Serving with the steak

Once you have imported Instagram data into a SQLite database file you can browse your data using [Datasette](https://github.com/simonw/datasette). Install Datasette like so:

    $ pip install datasette

Next run

```bash
datasette insta-chats.db -o
```

If you're new to SQL but still want to see what you could do with this, then

1. Find out what was the first message ever sent on any of your instagram chat rooms*

```sql
SELECT
    chat_room "Room", sender_name "Sender", coalesce(content, share, photos, videos, users, audio_files) "Message"
FROM
    chats_messages
GROUP BY
    chat_room
HAVING
    min(timestamp_ms)
ORDER BY
    timestamp_ms
```

Chat rooms refer to any regular, cross-platform or group chat.


2. Awhhgee, how about the second messages? A bit unrealistic but still...maybe you really have to KNOW

```sql
WITH ordered_messages
     AS (SELECT *,
                Row_number()
                  OVER (
                    partition BY chat_room
                    ORDER BY timestamp_ms) AS 'rank'
         FROM   chats_messages
         )
SELECT
    chat_room "Room", sender_name "Sender", coalesce(content, share, photos, videos, users, audio_files) "Message"
FROM
    ordered_messages
WHERE
    rank = 2
ORDER BY
    timestamp_ms ASC
```

3. Okay cool, what if I just want to start reading my chats from their inception like a...normal person...?

```sql
SELECT
    type, sender_name, DATETIME(ROUND(timestamp_ms / 1000), 'unixepoch') "Date", coalesce(content, share, photos, videos, users, audio_files) "Message"
FROM
    chats_messages
WHERE
    chat_room = '{chat_room}'
ORDER BY
    timestamp_ms
```

You will have to figure out the chat_room ID you want to query, but it won't be hard to figure that out.

## References

* Read more about datasette in [the docs](https://docs.datasette.io/en/stable/).

* Checkout the [dogsheep project](https://dogsheep.github.io) if you're interested in building your personal data warehouse ;)

## Pending stuff

This is the rest of the data available in the Instagram takeout that I haven't built import tools for, yet. Currently, only chat data is covered.

```json
{
    "login_and_account_creation": [
        "login_activity.json", "logout_activity.json",
        "signup_information.json", "password_change_activity.json",
        "account_privacy_changes.json"
    ],
    "shopping": ["recently_viewed_items.json"],
    "comments": ["post_comments.json", "comments_reported.json"],
    "device_information": ["camera_information.json", "devices.json"],
    "ads_and_content": [
        "suggested_accounts_viewed.json", "ads_viewed.json",
        "posts_viewed.json", "videos_watched.json", "ads_clicked.json"
    ],
    "information_about_you": ["account_based_in.json", "ads_interests.json"],
    "likes": ["liked_posts.json", "liked_comments.json"],
    "content": [
        "posts_1.json", "profile_photos.json", "stories.json",
        "archived_posts.json", "other_content.json",
        "recently_deleted_content.json"
    ],
    "your_topics": [
        "your_reels_topics.json", "your_topics.json",
        "your_reels_sentiments.json"
    ],
    "story_sticker_interactions": [
        "emoji_reactions.json", "quizzes.json", "questions.json",
        "emoji_sliders.json", "polls.json"
    ],
    "comments_settings": ["use_cross-app_messaging.json", "comments_allowed_from.json"],
    "recent_searches": ["tag_searches.json", "account_searches.json"],
    "saved": ["saved_collections.json", "saved_posts.json"],
    "followers_and_following": [
        "removed_suggestions.json", "following_hashtags.json",
        "following.json", "followers.json", "recent_follow_requests.json",
        "pending_follow_requests.json", "close_friends.json"
    ],
    "account_information": [
        "account_information.json", "profile_changes.json",
        "personal_information.json"
    ]
}
```