import json
import os
import praw
import time

# Try to import config class
try:
    from env import Config
except ImportError:
    print('Import Error')


class Bot:
    CONFIG_PATH = 'config.json'

    def __init__(self):
        self.reddit = self.load_reddit()
        self.config = self.load_notification_configuration(self.CONFIG_PATH)

    def load_reddit(self):
        #  needed variables
        Config.set_env_vars()

        reddit = praw.Reddit(client_id=os.environ['REDDIT_CLIENT_ID'],
                             client_secret=os.environ['REDDIT_CLIENT_SECRET'],
                             user_agent=os.environ['REDDIT_USER_AGENT'],
                             username=os.environ['REDDIT_USERNAME'],
                             password=os.environ['REDDIT_PASSWORD'])

        return reddit

    def find_submissions(self):
        # Use a multireddit to stream from multiple subreddits
        multireddit = '+'.join(self.config.keys())

        # Stream the multireddit, set skip_existing to True to skip any posts that are already in the sub
        for submission in self.reddit.subreddit(multireddit).stream.submissions(skip_existing=True):
            # Finds the subreddit, and loads the correct config.
            subreddit = submission.subreddit.display_name
            subreddit_data = self.config[subreddit]

            # Pull keywords out of the config file
            blacklisted_keywords = subreddit_data['blacklisted_keywords']
            keywords = subreddit_data['keywords']

            # Let the bot notify on all posts if keywords are empty
            notify_on_all_posts = len(keywords) < 1

            # Join submission and title
            target_text = ' '.join([submission.title, submission.selftext]).lower()

            # Check blacklist first, we will always search for all blacklisted keywords
            if not self.has_keyword(target_text, blacklisted_keywords) and (notify_on_all_posts or self.has_keyword(target_text, keywords)):
                # Message the redditors from the config if this check passes
                redditors = subreddit_data['redditors']

                for redditor in redditors:
                    # Check if the post author is the same as the targeted redditor
                    if not submission.author.name == redditor:
                        self.send_message(submission, redditor)

    def has_keyword(self, target_text, keywords):
        # Check if a keyword is in the target
        for keyword in keywords:
            if keyword.lower() in target_text:
                return True

        return False

    def send_message(self, submission, username):
        # Build up a good title
        title = "{}: {}".format(submission.subreddit.display_name, submission.title)

        # Check if it's too big, and trim it if so
        if len(title) > 100:
            title = title[:97] + '...'

        # Build the message body
        newlines = "\n\n" if submission.is_self else ''
        message_body = submission.selftext + newlines + 'Link: ' + submission.shortlink

        try:
            self.reddit.redditor(username).message(title, message_body)
            # Some screen printing to make sure everything works
            print('Sent new message')
            print('New post in {}, Title: {}, Description: {}'.format(
                submission.subreddit.display_name, submission.title, submission.selftext))
        except Exception as e:
            print(e)
            time.sleep(60)

    def load_notification_configuration(self, path):
        # Reads a JSON file to pull out notification configuration.
        # We can treat this as a dict, rather than multiple nested arrays that need to be tracked.
        with open(path) as f:
            data = json.load(f)

        return data


if __name__ == '__main__':
    Bot().find_submissions()
