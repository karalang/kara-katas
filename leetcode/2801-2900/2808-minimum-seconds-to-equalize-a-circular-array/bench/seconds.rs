// LeetCode #2808: Minimum Seconds to Equalize a Circular Array -- the
// bench in Rust: the ★ arm over 20 arrays of 10^5 numbers from 1000
// values, all drawn first, then each answered 20 times; the places in a
// `HashMap<i64, Vec<i64>>`.
use std::collections::HashMap;

fn minimum_seconds(nums: &[i64]) -> i64 {
    let n = nums.len() as i64;
    let mut places: HashMap<i64, Vec<i64>> = HashMap::new();
    for (i, &v) in nums.iter().enumerate() {
        places.entry(v).or_insert_with(Vec::new).push(i as i64);
    }
    let mut best = n;
    for at in places.values() {
        let mut widest = at[0] + n - at[at.len() - 1];
        for k in 1..at.len() {
            widest = widest.max(at[k] - at[k - 1]);
        }
        best = best.min(widest / 2);
    }
    best
}

struct Rng(i64);

impl Rng {
    fn next_random(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
    fn wide(&mut self) -> i64 {
        let a = self.next_random();
        a * 32768 + self.next_random()
    }
}

fn main() {
    let count = 20;
    let rounds = 20;
    let mut rng = Rng(2808);
    let mut cases = Vec::new();
    for _ in 0..count {
        let nums: Vec<i64> = (0..100000).map(|_| rng.wide() % 1000 * 1000003 + 1).collect();
        cases.push(nums);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for nums in &cases {
            let a = minimum_seconds(nums);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    println!("{count} arrays of 10^5, {rounds} rounds: seconds sum to {total}, checksum {check}");
}
