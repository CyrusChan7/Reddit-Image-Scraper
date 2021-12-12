import praw
import requests
import cv2
import numpy as np
import os
import pickle
import sys
import time

from utils.create_pickle_token import create_pickle_token


#If reddit.token does NOT exist, then help the user create it
def load_token():
    TOKEN_FILE_NAME = "reddit.token"
    if os.path.exists(TOKEN_FILE_NAME):
        with open(TOKEN_FILE_NAME, "rb") as token:
            credentials = pickle.load(token)
            return credentials
    else:
        credentials = create_pickle_token()
        pickle_out_file = open(TOKEN_FILE_NAME, "wb")
        pickle.dump(credentials, pickle_out_file)
        print(f"{TOKEN_FILE_NAME} has been generated successfully, please restart the program to continue. Exiting automatically in 10 seconds.")
        time.sleep(10)
        sys.exit()


def initialize_scraper():
    dir_path = os.path.dirname(os.path.abspath(__file__))   # Project root
    #print(f"DEBUG: dir_path is {dir_path}")
    os.chdir(dir_path)

    user_search_count = int(input(f"How many images to download? (If you specify 50, there may only be 35 images downloaded, because not every post contains an image): "))
    return user_search_count


reddit_credentials = load_token()
post_search_count = initialize_scraper()

# From official documentation
reddit = praw.Reddit(client_id=reddit_credentials["client_id"],
                         client_secret=reddit_credentials["client_secret"],
                         user_agent=reddit_credentials["user_agent"],
                         username=reddit_credentials["username"],
                         password=reddit_credentials["password"])


# Search as many subreddits as the user wants, one subreddit per line
spreadsheet = open("subreddits.csv", "r")
for sub in spreadsheet:

    subreddit = reddit.subreddit(sub.strip())
    print(f"Begin scraping subreddit: {sub.strip()}")

    count = 0
    for submission in subreddit.hot(limit=post_search_count):
        picture_formats = ["jpg", "jpeg", "png"]
        post_string = submission.url.lower()

        if any(pic in post_string for pic in picture_formats):

            # Save image
            response = requests.get(submission.url.lower(), stream=True).raw
            image = np.asarray(bytearray(response.read()), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            cv2.imwrite(f"images/{sub}-{submission.id}.png", image)
                
            count += 1
print("Scraping has finished successfully.")