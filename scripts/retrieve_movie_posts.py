import praw
from dotenv import load_dotenv
import os


def retrieve_movie_posts():
    load_dotenv()   # Load credentials from .env file

    reddit = praw.Reddit(
        client_id=os.getenv('client_id'),
        client_secret=os.getenv('client_secret'),
        user_agent=os.getenv('user_agent')
    )

    for submission in reddit.subreddit('movies').top(time_filter='hour'):
        print('Title:', submission.title)
        print('Text:', submission.selftext)
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            print(comment.body)
        print('-----------------------')


if __name__ == '__main__':
    retrieve_movie_posts()
