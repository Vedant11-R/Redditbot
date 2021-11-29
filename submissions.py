import praw
import time
import prawcore

reddit = praw.Reddit('bot', user_agent='cs40')

count=0
for submission in reddit.subreddit("conservative").hot(limit=None):
    a=submission.title
    b=submission.url
    try:
       reddit.subreddit('BotTown2').submit(a,url=b)
    except (praw.exceptions.RedditAPIException, prawcore.exceptions.NotFound) as e :
        pass
    count+=1
    print('reposted comments=',count)
    time.sleep(20)