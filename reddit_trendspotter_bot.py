#REDDIT BOT - Logs into reddit, extracts lists of top 10 trending subreddits for the day, week and month, and MILDLYtrending subreddit for the week
#Tailored by JavierMarti.co.uk

import praw
import time
import reddit_config


from urllib.parse import quote_plus


#login and choose subreddit/s
def main():
    #LOGIN
    reddit = praw.Reddit(user_agent = reddit_config.user_agent,
                         client_id = reddit_config.client_id,
                         client_secret = reddit_config.client_secret,
                         username = reddit_config.username,
                         password = reddit_config.password)

    print('\n')
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    print('Starting program and fetching submissions to subreddits...')
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n')


    subreddits_to_check = ['TrendingReddits']


# CHOOSE SUBREDDIT AND WHAT TO DO WITH EACH SUBMISSION
# limit is the NUMBER OF POSTS we want to include
    for el in subreddits_to_check:
        print('TOP LINKS IN', el, 'subreddit in the PAST 24H')
        print('------------------------------------------------------------')
        for submission in reddit.subreddit(el).top(time_filter= 'day', limit=20):
            process_submission(submission)




#TOP LINKS LAST WEEK

    for el in subreddits_to_check:
        print('TOP LINKS IN', el, 'subreddit in the LAST WEEK')
        print('------------------------------------------------------------')
        for submission in reddit.subreddit(el).top(time_filter= 'week', limit=10):
            process_submission(submission)

        print('\n')


# TOP LINKS LAST MONTH

    for el in subreddits_to_check:
        print('TOP LINKS IN', el, 'subreddit in the LAST MONTH')
        print('------------------------------------------------------------')
        for submission in reddit.subreddit(el).top(time_filter= 'month', limit=10):
            process_submission(submission)

        print('\n')


# TOP LINKS MILDLY TRENDING

    for el in subreddits_to_check:
        print('_______________________________________________________________________\n')
        print('TOP LINKS IN', el, 'subreddit in the LAST WEEK that are MILDLY TRENDING')
        print('------------------------------------------------------------')
        for submission in reddit.subreddit(el).top(time_filter='week', limit=10):
            process_submission_MILDLYTRENDING(submission)

        print('\n')


#initiate submission process and record results
def process_submission(submission):

        normalized_title = submission.title.lower()
        if submission.stickied == False:
            if '[TRENDING]' in submission.title:
                #print(normalized_title)
                #print(submission.subreddit.display_name)
                print(submission.title.split('-')[0].split(']')[1])
                print(submission.title.split('-')[1])
                print(submission.title.split('(')[1])
                print(submission.url)

                print('\n')


def process_submission_MILDLYTRENDING(submission):

        normalized_title = submission.title.lower()
        if submission.stickied == False:
            if '[Mildly Trending]' in submission.title:
                # print(normalized_title)
                # print(submission.subreddit.display_name)
                print(submission.title.split('-')[0].split(']')[1])
                print(submission.title.split('-')[1])
                print(submission.title.split('(')[1])
                print(submission.url)

                print('\n')

                        # # open txt file, verify and write each submission to file
                        # with open('changetonameoffile.txt', 'r') as cache:  # go through all cached posts
                        #     existing = cache.read().splitlines()
                        # # write new found questions if not already on file
                        # with open('reddit_bot_records.txt', 'a+') as cache:  # with cache open
                        #     if normalized_title not in existing:
                        #         print(thread_title)

                        #         time.sleep(6)
                        #
                        #         cache.write(normalized_title)
                        #         cache.write('\n')
                        #         print('.......................')
                        #         print('ADDING TO TEXTFILE >> ', thread_title)
                        #         print(submission.url,'\n')
                        #         time.sleep(0.5)

#Print 'mildly trending' entries
print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

#Start program if not already started
# if name == '__main__':
main()

#LEARN MORE about a trending subreddit
learn_more = input('Would you like to explore a subreddit or trend in more detail? If so, simply enter the name of the subreddit here: \n')
print(learn_more)
print('Thank you. To learn more simply click on these links:')

print('http://redditmetrics.com/r/'+ (learn_more))
print('https://trends.google.com/trends/explore?q='+ (learn_more))



