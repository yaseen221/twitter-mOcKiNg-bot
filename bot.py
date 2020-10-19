from keys import *
import tweepy
import json
import random

def from_creator(status):
    if hasattr(status, 'retweeted_status'):
        return False
    elif status.in_reply_to_status_id != None:
        return False
    elif status.in_reply_to_screen_name != None:
        return False
    elif status.in_reply_to_user_id != None:
        return False
    else:
        return True


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        if from_creator(tweet):
            text = tweet.text
            tags = []

            for word in text.split():
                if word.startswith('#'):
                    tags.append(word)

            text = ' '.join([word for word in text.split() if not word.startswith(('@', '#'))])

            mock_text = ''.join([c.upper() if not i%2 else c for i,c in enumerate(text.lower())])

            t = ' '.join(tags)
            
            # mock_text = ''.join([c.upper() if random.randint(0,1) else c for i,c in enumerate(text.lower())])
            api.update_status(f"{mock_text} {t}", in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
    
    def on_error(self, status):
        print("Error detected")


auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

tweets_listener = MyStreamListener(api)
stream = tweepy.Stream(api.auth, listener=tweets_listener)

stream.filter(follow=['25073877'], is_async=True)