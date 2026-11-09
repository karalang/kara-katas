// LeetCode #2034: Stock Price Fluctuation -- the ★ arm in Rust, the same
// algorithm and workload as stock.kara: a HashMap of prices, the latest
// timestamp, and two heaps of (price, timestamp) records with stale ones
// popped at query time.
use std::cmp::Reverse;
use std::collections::{BinaryHeap, HashMap};

struct StockPrice {
    prices: HashMap<i64, i64>,
    latest: i64,
    highs: BinaryHeap<(i64, i64)>,
    lows: BinaryHeap<Reverse<(i64, i64)>>,
}

impl StockPrice {
    fn new() -> Self {
        StockPrice { prices: HashMap::new(), latest: 0, highs: BinaryHeap::new(), lows: BinaryHeap::new() }
    }

    fn update(&mut self, timestamp: i64, price: i64) {
        self.prices.insert(timestamp, price);
        self.latest = self.latest.max(timestamp);
        self.highs.push((price, timestamp));
        self.lows.push(Reverse((price, timestamp)));
    }

    fn current(&self) -> i64 {
        self.prices[&self.latest]
    }

    fn maximum(&mut self) -> i64 {
        loop {
            let (price, timestamp) = *self.highs.peek().unwrap();
            if self.prices[&timestamp] == price {
                return price;
            }
            self.highs.pop();
        }
    }

    fn minimum(&mut self) -> i64 {
        loop {
            let Reverse((price, timestamp)) = *self.lows.peek().unwrap();
            if self.prices[&timestamp] == price {
                return price;
            }
            self.lows.pop();
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2034;
    let mut sessions: Vec<Vec<(i64, i64, i64)>> = Vec::new();
    for a in 0..10usize {
        let span = [1000000000, 100000, 1000, 1000000000, 50000][a % 5];
        let top = [1000000000, 1000, 1000000000, 100, 1000000][a % 5];
        let upd = (a % 7 + 2) as i64;
        let mut ops = Vec::new();
        for i in 0..100000 {
            if i == 0 || next_random(&mut seed) % 10 < upd {
                let hi = next_random(&mut seed);
                let lo = next_random(&mut seed);
                let timestamp = (hi * 32768 + lo) % span + 1;
                let hi = next_random(&mut seed);
                let lo = next_random(&mut seed);
                let price = (hi * 32768 + lo) % top + 1;
                ops.push((0, timestamp, price));
            } else {
                ops.push((next_random(&mut seed) % 3 + 1, 0, 0));
            }
        }
        sessions.push(ops);
    }
    let (mut runs, mut queries, mut check) = (0i64, 0i64, 0i64);
    for _ in 0..15 {
        for ops in &sessions {
            let mut stock = StockPrice::new();
            for &(kind, timestamp, price) in ops {
                if kind == 0 {
                    stock.update(timestamp, price);
                } else {
                    let answer = match kind {
                        1 => stock.current(),
                        2 => stock.maximum(),
                        _ => stock.minimum(),
                    };
                    queries += 1;
                    check = (check * 31 + answer % 1000000007 + kind) % 1000000007;
                }
            }
            runs += 1;
        }
    }
    println!("{} sessions: {} queries, checksum {}", runs, queries, check);
}
