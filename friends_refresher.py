from datetime import datetime
from itertools import izip_longest

import db
from twitter import Twitter
from user import User


class FriendsRefresher:
    def __init__(self, user, twitter=None):
        self.user = user
        self.twitter = twitter or user.twitter

    def run(self):
        if self.user.is_stale:
            self.refresh_friends()
        self.hydrate_friends()
        self.refresh_stale_friends()

    def refresh_friends(self):
        ids = self.twitter.friends_ids(self.user.twitter_id)
        self.user.friend_ids = ids
        db.session.commit()

    def hydrate_friends(self):
        self.user.create_friends()
        self.hydrate_users(self.user.dehydrated_friends)

    def refresh_stale_friends(self):
        for friend in self.user.stale_friends:
            twitter = friend.twitter or self.twitter
            self.__class__(friend, twitter).refresh_friends()

    def hydrate_users(self, users):
        ids = [user.twitter_id for user in users]
        chunks = izip_longest(*([iter(ids)] * Twitter.USERS_LOOKUP_CHUNK_SIZE))
        for chunk in chunks:
            self.hydrate_chunk(chunk)

    def hydrate_chunk(self, chunk):
        ids = [id for id in chunk if id is not None]
        profiles = self.twitter.users_lookup(ids)
        for profile in profiles:
            user = User.query.filter(User.twitter_id == profile['id']).scalar()
            user.raw = profile
            # user.screen_name = profile['screen_name']
            # user.last_tweet_at = datetime.strptime(
            #     profile['status']['created_at'],
            #     '%a %b %d %X +0000 %Y')
        db.session.commit()
