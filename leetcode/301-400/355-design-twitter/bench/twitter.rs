// Bench for LeetCode #355 -- Rust mirror of twitter.kara (the starred arm):
// per-user tweet lists merged newest-first through a priority queue.
use std::collections::{BinaryHeap, HashMap, HashSet};

const USERS: i64 = 1000;
const POSTS: i64 = 300000;
const FOLLOWS: i64 = 100000;
const FEEDS: i64 = 300000;

struct Twitter {
    clock: i64,
    tweets: HashMap<i64, Vec<(i64, i64)>>,
    follows: HashMap<i64, HashSet<i64>>,
}

impl Twitter {
    fn new() -> Self {
        Twitter { clock: 0, tweets: HashMap::new(), follows: HashMap::new() }
    }

    fn post_tweet(&mut self, user: i64, tweet: i64) {
        self.clock += 1;
        self.tweets.entry(user).or_insert_with(Vec::new).push((self.clock, tweet));
    }

    fn news_feed(&self, user: i64) -> Vec<i64> {
        let mut authors = vec![user];
        if let Some(followed) = self.follows.get(&user) {
            for &f in followed {
                if f != user {
                    authors.push(f);
                }
            }
        }
        // (time, tweet, author, index); BinaryHeap is largest-first.
        let mut queue: BinaryHeap<(i64, i64, i64, i64)> = BinaryHeap::new();
        for a in authors {
            if let Some(list) = self.tweets.get(&a) {
                if !list.is_empty() {
                    let last = list.len() - 1;
                    queue.push((list[last].0, list[last].1, a, last as i64));
                }
            }
        }
        let mut feed = Vec::new();
        while feed.len() < 10 {
            match queue.pop() {
                Some((_, tweet, author, i)) => {
                    feed.push(tweet);
                    if i > 0 {
                        let older = self.tweets[&author][(i - 1) as usize];
                        queue.push((older.0, older.1, author, i - 1));
                    }
                }
                None => break,
            }
        }
        feed
    }

    fn follow(&mut self, follower: i64, followee: i64) {
        self.follows.entry(follower).or_insert_with(HashSet::new).insert(followee);
    }
}

fn main() {
    let mut t = Twitter::new();
    let mut seed: i64 = 355;
    for i in 0..POSTS {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        t.post_tweet(seed % USERS, i);
    }
    for _ in 0..FOLLOWS {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let a = seed % USERS;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        t.follow(a, seed % USERS);
    }
    let mut sink: i64 = 0;
    for _ in 0..FEEDS {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        for id in t.news_feed(seed % USERS) {
            sink = (sink * 31 + id) % 1000000007;
        }
    }
    println!("{}", sink);
}
