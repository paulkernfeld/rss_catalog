from sources import add_source_interactive, url_to_name

REDDIT_NAME_URL = "http://www.reddit.com/r/{}"
REDDIT_URL = "https://reddit.com/r/{}.xml"


def add_subreddit(subreddit_name, info):
    add_source_interactive(
        url_to_name(REDDIT_NAME_URL.format(subreddit_name)),
        REDDIT_URL.format(subreddit_name),
        info
    )
