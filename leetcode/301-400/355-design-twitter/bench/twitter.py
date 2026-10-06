# Bench for LeetCode #355 -- Python mirror of twitter.kara (the starred arm):
# per-user tweet lists merged newest-first through a priority queue.
import heapq

USERS = 1000
POSTS = 300000
FOLLOWS = 100000
FEEDS = 300000


class Twitter:
    def __init__(self):
        self.clock = 0
        self.tweets = {}
        self.follows = {}

    def post_tweet(self, user, tweet):
        self.clock += 1
        self.tweets.setdefault(user, []).append((self.clock, tweet))

    def news_feed(self, user):
        authors = [user]
        for f in self.follows.get(user, ()):
            if f != user:
                authors.append(f)
        # heapq is smallest-first, so the time is negated for newest-first.
        queue = []
        for a in authors:
            lst = self.tweets.get(a)
            if lst:
                last = len(lst) - 1
                time, tweet = lst[last]
                heapq.heappush(queue, (-time, -tweet, -a, -last))
        feed = []
        while len(feed) < 10 and queue:
            _, tweet, author, index = heapq.heappop(queue)
            tweet, author, index = -tweet, -author, -index
            feed.append(tweet)
            if index > 0:
                time, older = self.tweets[author][index - 1]
                heapq.heappush(queue, (-time, -older, -author, -(index - 1)))
        return feed

    def follow(self, follower, followee):
        self.follows.setdefault(follower, set()).add(followee)

    def unfollow(self, follower, followee):
        if follower in self.follows:
            self.follows[follower].discard(followee)


def main():
    t = Twitter()
    seed = 355
    for i in range(POSTS):
        seed = (seed * 1103515245 + 12345) % 2147483648
        t.post_tweet(seed % USERS, i)
    for _ in range(FOLLOWS):
        seed = (seed * 1103515245 + 12345) % 2147483648
        a = seed % USERS
        seed = (seed * 1103515245 + 12345) % 2147483648
        t.follow(a, seed % USERS)
    sink = 0
    for _ in range(FEEDS):
        seed = (seed * 1103515245 + 12345) % 2147483648
        for tid in t.news_feed(seed % USERS):
            sink = (sink * 31 + tid) % 1000000007
    print(sink)


if __name__ == "__main__":
    main()
