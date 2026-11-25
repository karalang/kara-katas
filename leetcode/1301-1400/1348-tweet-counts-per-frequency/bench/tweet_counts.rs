// LeetCode #1348 bench -- Rust: each name's times in the order recorded;
// a query walks every time of its name into per-chunk counts.
use std::collections::HashMap;

struct TweetCounts {
    times: HashMap<String, Vec<i32>>,
}

impl TweetCounts {
    fn new() -> Self {
        TweetCounts { times: HashMap::new() }
    }

    fn record_tweet(&mut self, name: &str, time: i32) {
        self.times.entry(name.to_string()).or_default().push(time);
    }

    fn get_tweet_counts_per_frequency(&self, freq: &str, name: &str, start: i32, end: i32) -> Vec<i32> {
        let size = match freq {
            "minute" => 60,
            "hour" => 3600,
            _ => 86400,
        };
        let mut counts = vec![0i32; ((end - start) / size + 1) as usize];
        if let Some(times) = self.times.get(name) {
            for &t in times {
                if t >= start && t <= end {
                    counts[((t - start) / size) as usize] += 1;
                }
            }
        }
        counts
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let names = ["n0", "n1", "n2", "n3", "n4", "n5", "n6", "n7", "n8", "n9"];
    let freqs = ["minute", "hour", "day"];
    let mut seed = 1348;
    let mut tc = TweetCounts::new();
    for _ in 0..100000 {
        let name = names[(next_random(&mut seed) % 10) as usize];
        tc.record_tweet(name, (next_random(&mut seed) % 1000001) as i32);
    }
    let mut check: i64 = 0;
    for r in 0..10000i64 {
        tc.record_tweet(names[(check % 10) as usize], (check % 1000001) as i32);
        let start = (check / 11) % 990001;
        let counts = tc.get_tweet_counts_per_frequency(
            freqs[((check / 13) % 3) as usize],
            names[((check / 17) % 10) as usize],
            start as i32,
            (start + 10000) as i32,
        );
        for &n in &counts {
            check = (check * 31 + n as i64) % 1000000007;
        }
        check = (check * 31 + r) % 1000000007;
    }
    println!("10000 rounds over 100000 tweets: checksum {}", check);
}
