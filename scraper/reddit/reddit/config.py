from praw import Reddit
from pydantic import BaseSettings


class RedditConfig(BaseSettings):
    client_id: str
    client_secret: str
    password: str
    username: str


def connect_reddit(config: RedditConfig):
    return Reddit(
        user_agent=f"mychef by /u/{config.username}",
        client_id=config.client_id,
        client_secret=config.client_secret,
        password=config.password,
        username=config.username,
    )
