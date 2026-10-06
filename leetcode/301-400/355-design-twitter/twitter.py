# LeetCode #355: Design Twitter -- Python mirror of twitter.kara.
# Per-user tweet lists merged newest-first through a priority queue: start
# with each author's newest tweet, and every pop pushes that author's next
# older tweet, at most ten pops.
import heapq


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


def fmt(feed):
    return "[" + ", ".join(str(x) for x in feed) + "]"


def show(label, feed):
    print(f"{label}: {fmt(feed)}")


def main():
    t = Twitter()
    t.post_tweet(1, 5)
    show("example feed 1", t.news_feed(1))
    t.follow(1, 2)
    t.post_tweet(2, 6)
    show("example feed 2", t.news_feed(1))
    t.unfollow(1, 2)
    show("example feed 3", t.news_feed(1))

    e = Twitter()
    show("nobody has posted", e.news_feed(7))
    e.follow(7, 7)
    e.post_tweet(7, 70)
    show("following yourself shows each tweet once", e.news_feed(7))
    e.unfollow(7, 7)
    show("unfollowing yourself keeps your own tweets", e.news_feed(7))
    e.unfollow(7, 99)
    show("unfollowing a stranger is a no-op", e.news_feed(7))
    for i in range(15):
        e.post_tweet(8, 800 + i)
    e.follow(7, 8)
    show("only the ten newest", e.news_feed(7))
    e.post_tweet(7, 71)
    e.post_tweet(9, 90)
    e.follow(7, 9)
    show("interleaved authors", e.news_feed(7))
    e.follow(7, 9)
    show("following twice changes nothing", e.news_feed(7))
    show("a follower's view is not shared", e.news_feed(8))

    g = Twitter()
    seed = 355
    checksum = 0
    feeds = 0
    next_tweet = 1000
    for step in range(20000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        op = (seed // 65536) % 10
        seed = (seed * 1103515245 + 12345) % 2147483648
        a = (seed // 65536) % 40
        seed = (seed * 1103515245 + 12345) % 2147483648
        b = (seed // 65536) % 40
        if op < 4:
            g.post_tweet(a, next_tweet)
            next_tweet += 1
        elif op < 6:
            g.follow(a, b)
        elif op < 7:
            g.unfollow(a, b)
        else:
            feed = g.news_feed(a)
            feeds += 1
            for tid in feed:
                checksum = (checksum * 31 + tid) % 1000000007
            checksum = (checksum * 31 + step) % 1000000007
    print(f"20000 random operations: {feeds} feeds, {next_tweet - 1000} tweets, checksum {checksum}")


if __name__ == "__main__":
    main()
