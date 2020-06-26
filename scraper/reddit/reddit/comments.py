from typing import Iterator, Dict

import jsonlines

from tqdm import tqdm
from praw import Reddit
from praw.models.reddit.comment import Comment
from praw.models.listing.generator import ListingGenerator


class RedditComments:
    """Extract all top level comments from top posts for a given subreddit(s)"""

    def __init__(self, reddit: Reddit, subreddit: str, n_posts: int):
        self.reddit = reddit
        self.subreddit = subreddit
        self.n_posts = n_posts

    def __repr__(self) -> str:
        return f"TopComments(subreddit='{self.subreddit}', limit={self.limit})"

    def get_posts(self) -> ListingGenerator:
        return self.reddit.subreddit(self.subreddit).top(limit=self.n_posts)

    def get_comments(self) -> Iterator[Dict[str, str]]:
        posts = self.get_posts()
        return ({"text": self._extract_comment(c)} for p in posts for c in p.comments)

    def _extract_comment(self, comment: Comment) -> str:
        try:
            return comment.body.replace("\n", " ").replace("\t", " ")
        except AttributeError:
            return None

    @staticmethod
    def save_comments(comments: Iterator[Dict["str", "str"]], filename: str):
        assert filename.split('.')[-1] == 'jsonl'
        with jsonlines.open(filename, mode="w") as writer:
            for _, comment in enumerate(tqdm(comments)):
                reddit_comment = comment["text"]
                if reddit_comment and len(reddit_comment) > 150:
                    writer.write(comment)
