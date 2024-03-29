# Reddit Notification Bot

A reddit bot that messages the user when a new post containing a keyword appears in one of the specified subreddits. It supports messaging multiple redditors, multiple keywords, blacklisted keywords over multiple subreddits. The configuration details (REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET etc.) are to be specified in the env.py file. The specifications of the bot (desired subreddits, keywords, blacklisted keywords) are to be specified the .json file. Examples of possible .json file content formats:

# Example 1
```
{
  "science": {
    "keywords": [
      "Covid",
      "Cancer"
    ],
    "blacklisted_keywords": [
    ],
    "redditors": [
      "redditor_1",
      "redditor_2"
    ]
  }
}
```
When either of the keywords "Covid" or "Cancer" appear in a post's title or body in the subreddit r/science, the bot messages users "redditor_1" and "redditor_2"

# Example 2
```
{
  "politics": {
    "keywords": [
      "Gonverment"
    ],
    "blacklisted_keywords": [
      "USA",
      "China"
    ],
    "redditors": [
      "redditor_1",
      "redditor_3"
    ]
  }
}
```
When the keyword "Gonverment" appear in a post's title or body in the subreddit r/politics and the words "USA" and "China" don't, the bot messages users "redditor_1" and "redditor_3"

# Example 3
```
{
  "requestabot": {
    "keywords": [
    ],
    "blacklisted_keywords": [
    ],
    "redditors": [
      "redditor_1"
    ]
  }
}
```
Every time any new post is posted in the subreddit r/requestabot, the bot messages the user "redditor_1"
