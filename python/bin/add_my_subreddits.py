#!/usr/bin/env python
import json
from sys import argv

from rss_catalog.reddit import add_subreddit


# Works on the output of https://www.reddit.com/subreddits/mine.json
# As the first argument, pass in the path to a data file.

json_file = argv[1]
data = json.load(open(json_file))
subreddits = [subreddit['data'] for subreddit in data['data']['children']]

if len(subreddits) == 50:
    print("Warning: Exactly 50 subreddits detected. You probably need to change your pagination settings to export all "
          "your subreddits.")

for subreddit in subreddits:
    info = "subscribers: {}".format(subreddit['subscribers'])
    if subreddit['over18'] != False:
        info = 'WARNING: over18={}\n{}'.format(subreddit['over18'], info)
    if subreddit['subreddit_type'] != 'public':
        info = 'WARNING: subreddit_type={}\n{}'.format(subreddit['subreddit_type'], info)

    add_subreddit(subreddit['url'][3:-1], info)