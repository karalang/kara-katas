// LeetCode #2898: Maximum Linear Stock Score -- the bench's Rust mirror
// (stock.kara): a std HashMap, its default SipHash, as Kāra's Map.

use std::collections::HashMap;

fn max_score(prices: &[i64]) -> i64 {
    let mut sums: HashMap<i64, i64> = HashMap::new();
    for (i, &p) in prices.iter().enumerate() {
        *sums.entry(p - i as i64).or_insert(0) += p;
    }
    *sums.values().max().unwrap()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn main() {
    let (count, rounds, n) = (20i64, 20i64, 100000i64);
    let mut seed = 2898i64;
    let mut cases: Vec<Vec<i64>> = Vec::new();
    for c in 0..count {
        let mut prices = Vec::new();
        for i in 0..n {
            if c % 2 == 0 {
                prices.push(wide(&mut seed) % 1000000000 + 1);
            } else {
                prices.push(1000000 + i - next_random(&mut seed) % 50);
            }
        }
        cases.push(prices);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for prices in &cases {
            let score = max_score(prices);
            total += score;
            check = (check * 31 + score % 1000000007 + r) % 1000000007;
        }
    }
    println!("{count} arrays of {n}, {rounds} rounds: scores total {total}, checksum {check}");
}
