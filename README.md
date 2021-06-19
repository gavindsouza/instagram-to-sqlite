# instagram-to-sqlite

<!--

[![PyPI](https://img.shields.io/pypi/v/instagram-to-sqlite.svg)](https://pypi.org/project/instagram-to-sqlite/)
[![GitHub Actions]()]()
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/gavindsouza/instagram-to-sqlite/blob/master/LICENSE)

-->

Save data from a Instagram takeout to a SQLite database.


## Installation

```bash
git clone https://github.com/gavindsouza/instagram-to-sqlite
pip install -e ./instagram-to-sqlite
```

This tool only supports JSON data takeouts.

## Something

    $ instagram-to-sqlite chats insta-chats.db ~/Downloads/takeout-20190530.zip

This will create a database file called `insta-chats.db` if one does not already exist.


## Browsing your data with Datasette

Once you have imported Instagram data into a SQLite database file you can browse your data using [Datasette](https://github.com/simonw/datasette). Install Datasette like so:

    $ pip install datasette

Next run

```bash
datasette insta-chats.db -o
```

Read more about datasette in [the docs](https://docs.datasette.io/en/stable/).

## Pending stuff

```json
other_data = {
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