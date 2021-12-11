import praw
import requests
import cv2
import numpy as np
import os
import pickle

from utils.create_pickle_token import create_pickle_token


def load_token():
    if os.path.exists("reddit.token"):
        with open("reddit.token", "rb") as token:
            credentials = pickle.load(token)
            return credentials
    else:
        credentials = create_pickle_token()
        pickle_out_file = open("reddit.token","wb")
        pickle.dump(credentials, pickle_out_file)


def initialize_scraper():
    dir_path = os.path.dirname(os.path.abspath(__file__))   # Project root
    #print(f"DEBUG: dir_path is {dir_path}")
    os.chdir(dir_path)

    user_search_count = int(input("How many posts would you like to search? (Enter a number): "))
    return user_search_count


reddit_credentials = load_token()
post_search_count = initialize_scraper()


reddit = praw.Reddit(client_id=reddit_credentials["client_id"],
                         client_secret=reddit_credentials["client_secret"],
                         user_agent=reddit_credentials["user_agent"],
                         username=reddit_credentials["username"],
                         password=reddit_credentials["password"])


spreadsheet = open("subreddits.csv", "r")
for sub in spreadsheet:

    subreddit = reddit.subreddit(sub.strip())
    print(f"Begin scraping subreddit: {sub.strip()}")
    count = 0
    for submission in subreddit.hot(limit=post_search_count):
        if "jpg" in submission.url.lower() or "png" in submission.url.lower():
            response = requests.get(submission.url.lower(), stream=True).raw
            image = np.asarray(bytearray(response.read()), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)

            cv2.imwrite(f"images/{sub}-{submission.id}.png", image)
            count += 1