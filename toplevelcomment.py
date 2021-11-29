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


submission_url = 'https://old.reddit.com/r/BotTown2/comments/r0yi9l/main_discussion_thread/?'
submission = reddit.submission(url=submission_url)

while True:

    print()
    print('new iteration at:',datetime.datetime.now())
    print('submission.title=',submission.title)
    print('submission.url=',submission.url)
    submission.comments.replace_more(limit=None)
    all_comments = submission.comments.list()
    
    print('len(all_comments)=',len(all_comments))

    not_my_comments = []
    for comment in all_comments:
        if str(comment.author) != 'Vedant11bott':
            not_my_comments.append(comment)

    print('len(not_my_comments)=',len(not_my_comments))
    try:
        if len(not_my_comments) == len(all_comments):
            top_comment = not_my_comments[0]
            for tlc in submission.comments:
                if str(tlc.author) != 'Vedant11bott' and int(tlc.score) > top_comment.score:
                    top_comment = tlc
            text = generate_comment()
            top_comment.reply(text)

        else:
            comments_without_replies = []
            not_yet_commented = False
            for comment in not_my_comments:
                try:
                    comment.refresh()
                    for reply in comment.replies:
                        if str(reply.author) == 'Vedant11bott':
                            not_yet_commented = False
                            break
                        else:
                            not_yet_commented = True
                except(AttributeError, praw.exceptions.ClientException):
                    pass
                if not_yet_commented:
                    comments_without_replies.append(comment)
            print('len(comments_without_replies)=',len(comments_without_replies))

            if len(comments_without_replies) > 0:
                comment = random.choice(comments_without_replies)
                comment.reply(generate_comment())

        possible_new_subs = []
        for submission in reddit.subreddit("BotTown2").hot(limit=5):
            possible_new_subs.append(submission)
        submission = random.choice(possible_new_subs)
        while str(submission.author) == "imtherealcs40bot":
            submission = random.choice(possible_new_subs)
        submission.comments.replace_more()
    except praw.exceptions.RedditAPIException:
        time.sleep(500) 