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
submission_url = 'https://old.reddit.com/r/BotTown_polibot2/comments/r1ltr2/rbottown_polibot2_lounge/'
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
    # printing the current time will help make the output messages more informative
    # since things on reddit vary with time
    print()
    print('new iteration at:',datetime.datetime.now())
    print('submission.title=',submission.title)
    print('submission.url=',submission.url)
    submission.comments.replace_more(limit=None)
    # FIXME (task 0): get a list of all of the comments in the submission
    # HINT: this requires using the .list() and the .replace_more() functions
    
    #submission.comments.replace_more(limit=None)
    all_comments = submission.comments.list()
    
    # HINT: 
    # we need to make sure that our code is working correctly,
    # and you should not move on from one task to the next until you are 100% sure that 
    # the previous task is working;
    # in general, the way to check if a task is working is to print out information 
    # about the results of that task, 
    # and manually inspect that information to ensure it is correct; 
    # in this specific case, you should check the length of the all_comments variable,
    # and manually ensure that the printed length is the same as the length displayed on reddit;
    # if it's not, then there are some comments that you are not correctly identifying,
    # and you need to figure out which comments those are and how to include them.
    print('len(all_comments)=',len(all_comments))

    # FIXME (task 1): filter all_comments to remove comments that were generated by your bot
    # HINT: 
    # use a for loop to loop over each comment in all_comments,
    # and an if statement to check whether the comment is authored by you or not
    not_my_comments = []
    for comment in all_comments:
        #print('comment.author=', comment.author)
        #print(type(comment.author)) #redditor
        if str(comment.author) != 'Vedant11bott':
            not_my_comments.append(comment)


    # HINT:
    # checking if this code is working is a bit more complicated than in the previous tasks;
    # reddit does not directly provide the number of comments in a submission
    # that were not gerenated by your bot,
    # but you can still check this number manually by subtracting the number
    # of comments you know you've posted from the number above;
    # you can use comments that you post manually while logged into your bot to know 
    # how many comments there should be. 
    print('len(not_my_comments)=',len(not_my_comments))

    # if the length of your all_comments and not_my_comments lists are the same,
    # then that means you have not posted any comments in the current submission;
    # (your bot may have posted comments in other submissions);
    # your bot will behave differently depending on whether it's posted a comment or not
    has_not_commented = len(not_my_comments) == len(all_comments)
    print('has_not_commented=', has_not_commented)
   
    if has_not_commented:
        # FIXME (task 2)
        # if you have not made any comment in the thread, then post a top level comment
        #
        # HINT:
        # use the generate_comment() function to create the text,
        # and the .reply() function to post it to reddit;
        # a top level comment is created when you reply to a post instead of a message

        submission.reply(generate_comment())

    else:
        # FIXME (task 3): filter the not_my_comments list to also remove comments that 
        # you've already replied to
        # HINT:
        # there are many ways to accomplish this, but my solution uses two nested for loops
        # the outer for loop loops over not_my_comments,
        # and the inner for loop loops over all the replies of the current comment from the outer loop,
        # and then an if statement checks whether the comment is authored by you or not
        #comments_without_replies = not_my_comments
        # HINT:
        # this is the most difficult of the tasks,
        # and so you will have to be careful to check that this code is in fact working correctly

        comments_without_my_replies = []
        for comment in not_my_comments:
            if comment.author != 'Vedant11bott':
                response = False
                for reply in comment.replies:
                    if str(reply.author) == 'Vedant11bott':
                        response = True
                if response is False:
                    comments_without_my_replies.append(comment)
        print('Number of Comments Without My Replies: ', len(comments_without_my_replies))

        # FIXME (task 4): randomly select a comment from the comments_without_replies list,
        # and reply to that comment
        #
        # HINT:
        # use the generate_comment() function to create the text,
        # and the .reply() function to post it to reddit;
        # these will not be top-level comments;
        # so they will not be replies to a post but replies to a message

        for comments in comments_without_my_replies:
            selection = random.choice(comments_without_my_replies)
            generated_reply = generate_comment()
            try:
                selection.reply(generated_reply)
            except praw.exceptions.RedditAPIException as error:
                if "DELETED_COMMENT" in str(error):
                    print("Comment " + comment.id + " was deleted")
                else:
                    print('Error Found: ', error)

    # FIXME (task 5): select a new submission for the next iteration;
    # your newly selected submission should be randomly selected from the 5 hottest submissions
    randomnumber = random.random()
    allsubmissions = []
    if randomnumber >= 0.5:
        print('Original Submission')
        submission = reddit.submission(url='https://old.reddit.com/r/BotTown_polibot2/comments/r1ltr2/rbottown_polibot2_lounge/')
        submission.reply(generate_comment())
    if randomnumber < 0.5:
        print('Top Subreddit Submission')
        for submission in reddit.subreddit('BotTown_polibot2').hot(limit=5):
            allsubmissions.append(submission)
        newsubmission = random.choice(allsubmissions)
        submission = reddit.submission(id=newsubmission)
        print('Submission ID: ', newsubmission)
        print(newsubmission.title)
    time.sleep(750)

