import praw
import random
import datetime
import time
from textblob import TextBlob

reddit = praw.Reddit('bot', user_agent='cs40')

submission_url = 'https://www.reddit.com/r/BotTown2/comments/r0yi9l/main_discussion_thread/'
submission = reddit.submission(url='https://www.reddit.com/r/BotTown2/comments/r0yi9l/main_discussion_thread/')
 

while True:
    submission_text = TextBlob(submission.title)
    if ("crenshaw" in submission_text.lower() and submission_text.sentiment.polarity>0.5):
        submission.upvote()
    elif ("Trump" in submission_text.lower() and submission_text.sentiment.polarity>0.5):
        submission.downvote()