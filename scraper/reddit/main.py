from argparse import ArgumentParser

from reddit.comments import RedditComments
from reddit.config import RedditConfig, connect_reddit


def main(subreddit: str, n_posts: int, filename: str):
    # connect to reddit with credentials passed through .env file
    config = RedditConfig(_env_file="reddit.env")
    reddit = connect_reddit(config)

    # query comments from top posts based on subreddit and number of posts
    rc = RedditComments(reddit, subreddit, n_posts)
    comments = rc.get_comments()

    # save results to as .jsonl
    rc.save_comments(comments, filename)


def parser():
    parser = ArgumentParser(description="Extract reddit data")
    parser.add_argument("--subreddit", required=True, help="Subreddit(s) use + to join")
    parser.add_argument("--n_posts", type=int, default=10, help="# of posts to scrape")
    parser.add_argument("--filename", default="comments.jsonl", help="Output file")
    return parser.parse_args()


if __name__ == "__main__":
    args = parser()
    main(**vars(args))
