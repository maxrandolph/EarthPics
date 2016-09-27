# Quick script for getting top pics from r/EarthPorn

import praw
import re
import glob
import requests
from bs4 import BeautifulSoup
MIN_SCORE = 100

def downloadImage(imageUrl, localFileName):
    response = requests.get(imageUrl)
    if response.status_code == 200:
        print("download %s..." % (localFileName))
    with open(localFileName, 'wb') as fo:
        for chunk in response.iter_content(4096):
            fo.write(chunk)

user_agent = ("EarthPronBot")
r = praw.Reddit(user_agent = user_agent)
subreddit = r.get_subreddit("EarthPorn")
urlCheck = re.compile(r'(http:\/\/imgur\.com\/)([a-zA-Z0-9])+')

for submission in subreddit.get_hot(limit = 15):
    print(submission.url)
    if "imgur.com" not in submission.url and "i.redd.it" not in submission.url:
        continue
    if submission.score < MIN_SCORE:
        continue
    if len(glob.glob('reddit_%s_*' % (submission.id))) > 0:
        continue # we've already downloaded files for this reddit submission
    print(submission.url)
    if urlCheck.match(submission.url):
        submission.url = submission.url[:7] + "i." + submission.url[7:] + ".jpg"
    downloadImage(submission.url,submission.title+".jpg")
