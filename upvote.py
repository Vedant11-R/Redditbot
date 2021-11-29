import praw
import random
import datetime
import time
from textblob import TextBlob

# FIXME:
# copy your generate_comment function from the madlibs assignment here
madlibs = [
    "President Obama was an [AMAZING] president. Not a single person [DISLIKED] President Obama. He is an [IDOL] to millions not just in the United States but all around the world. During his presidency he [ACHIEVED] many [OUTSTANDING] feats.",
    "President Obama had a [PEACE_LOVING] [OUTLOOK]. He [HELPED] end war in Iraq. He [FORCED] all the [TROOPS] to leave Iraq",
    "President Obama was a [LIBERAL] [PRESIDENT]. When [SAME_SEX] marriages were [LOOKED_DOWN_ON] by many, he [LEGALIZED] it.",
    "President Obama had a [PEACE_LOVING] [OUTLOOK]. He [HELPED] [REDUCE] [TROOPS] in Afghanistan."
    "President Obama [BETTERED] the American [ECONOMY]. He [TURNED AROUND] the automobiles industry. He [RECAPTALIZED] [BANKS].",
    "[HE] was [LOVED] by the [WHOLE] world. [HE] [ASSISTED] many [COUNTRIES].",
    ]

replacements = {
    'AMAZING' : ['amazing', 'outstanding', 'astonishing'],
    'DISLIKED' : ['hated', 'detest', 'despised', 'disliked'],
    'IDOL' : ['idol', 'icon'],
    'ACHIEVED' : ['accomplished', 'achieved', 'executed'],
    'OUTSTANDING' : ['marvelous', 'outstnading', 'excellent', 'exceptional'],
    'PEACE_LOVING'  : ['peace loving', 'peaceful', 'tranquil'],
    'OUTLOOK' : ['attitude', 'point of view', 'outlook', 'nature'],
    'HELPED' : ['helped', 'succesfully', 'was able to'],
    'FORCED' : ['forced', 'ordered', 'commanded'],
    'TROOPS' : ['troops', 'forces', 'milliatry'],
    'LIBERAL' : ['open minded', 'liberal', 'broad minded'],
    'PRESIDENT' : ['president', 'leader', 'human'],
    'SAME_SEX' : ['same sex', 'homosexual', 'same gender'],
    'LOOKED_DOWN_ON' : ['looked down on', 'frowned upon', 'not supported'],
    'LEGALIZED' : ['legalized', 'supported', 'permitted'],
    'REDUCE' : ['reduce','lower the number of', 'minimized the number of'],
    'BETTERED' : ['bettered', 'improved', 'increased'],
    'ECONOMY' : ['GDP', 'economy'],
    'TURNED AROUND' : ['flipped', 'up-scaled', 'improved', 'turned around'],
    'RECAPTALIZED' : ['recaptalized, improved, bettered'],
    'BANKS' : ['banks', 'financial institutes'],
    'HE' : [ 'He', 'President Obama'],
    'LOVED' : ['loved', 'respected' , 'valued'],
    'WHOLE' : ['whole', 'entire'],
    'ASSISTED' : ['assisted', 'helped'],
    'COUNTRIES' : ['countries', 'nations'],
    }


def generate_comment():
    '''
    This function generates random comments according to the patterns specified in the `madlibs` variable.
    To implement this function, you should:
    1. Randomly select a string from the madlibs list.
    2. For each word contained in square brackets `[]`:
        Replace that word with a randomly selected word from the corresponding entry in the `replacements` dictionary.
    3. Return the resulting string.
    For example, if we randomly seleected the madlib "I [LOVE] [PYTHON]",
    then the function might return "I like Python" or "I adore Programming".
    Notice that the word "Programming" is incorrectly capitalized in the second sentence.
    You do not have to worry about making the output grammatically correct inside this function.
    '''
    s = random.choice(madlibs)
    for k in replacements.keys():
        s = s.replace('['+k+']', random.choice(replacements[k]))
    return s


# connect to reddit 
reddit = praw.Reddit('bot')


# select a "home" submission in the /r/BotTown subreddit to post to,
# and put the url below
submission_url = 'https://old.reddit.com/r/BotTown2/comments/r0yi9l/main_discussion_thread/'
submission = reddit.submission(url=submission_url)

# each iteration of this loop will post a single comment;
# since this loop runs forever, your bot will continue posting comments forever;
# (this is what makes it a deamon);
# recall that you can press CTRL-C in the terminal to stop your bot
#
# HINT:
# while you are writing and debugging your code, 
# you probably don't want it to run in an infinite loop;
# you can change this while loop to an if statement to make the code run only once
while True:
    print()
    print('new iteration at:',datetime.datetime.now())
    print('submission.title=',submission.title)
    print('submission.url=',submission.url)
    blob = TextBlob(submission.title)
    polarity = blob.sentiment.polarity
    if "Obama" in (submission.title).lower():
        if polarity > 0:
            submission.upvote() 
            print("Polarity =", str(polarity) + ".", "Submission upvoted")
        else:
            submission.upvote()
            print("Polarity =", str(polarity) + ".", "Submission upvoted!")
    if "Trump" in (submission.title).lower() or "Donald Trump" in (submission.title).lower():
        if polarity > 0:
            submission.downvote() #upvotes positive discussions of buttigieg
            print("Polarity =", str(polarity) + ".", "Submission downvoted")
        else:
            submission.upvote()
            print("Polarity =", str(polarity) + ".", "Submission upvoted")

    submission.comments.replace_more(limit=None)
    all_comments = submission.comments.list()
    print('len(all_comments) =', len(all_comments))
    
    upvotes = 0
    downvotes = 0
    
    for comment in all_comments:
        comment.refresh()
        try:
            if str(comment.author) != 'Vedant11bott':
                blob = TextBlob(comment.body)
                polarity = blob.sentiment.polarity
                if "Trump" in (comment.body).lower() or "Donald Trump" in (comment.body).lower():
                    if polarity > 0:
                        comment.downvote()
                        downvotes += 1
                    else:
                        comment.upvote()
                        upvotes += 1
                if "Obama" in (comment.body).lower():
                    if polarity > 0:
                        comment.upvote()
                        upvotes += 1
                    else:
                        comment.downvote()
                        downvotes += 1
            for reply in comment.replies:
                blob = TextBlob(reply.body)
                polarity = blob.sentiment.polarity
                if "Trump" in (reply.body).lower() or "Donald Trump" in (reply.body).lower():
                    if polarity > 0:
                        reply.downvote()
                        downvotes += 1
                    else:
                        reply.upvote()
                        upvotes += 1
                if "Obama" in (reply.body).lower():
                    if polarity > 0:
                        reply.upvote()
                        upvotes += 1
                    else:
                        reply.downvote()
                        downvotes += 1
        except(AttributeError, praw.exceptions.ClientException):
            pass
    print(upvotes, "comments upvoted.")
    print(downvotes, "comments downvoted.")
    
    possible_new_subs = []
    for submission in reddit.subreddit("BotTown2").hot(): 
        possible_new_subs.append(submission)
    submission = random.choice(possible_new_subs)
    submission.comments.replace_more()
    print()