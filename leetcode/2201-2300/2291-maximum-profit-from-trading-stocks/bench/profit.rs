// LeetCode #2291: Maximum Profit From Trading Stocks -- the bench, the ★
// arm in Rust. A 0/1 knapsack row over the budget, run downwards for each
// stock that gains.

fn maximum_profit(present: &[i64], future: &[i64], budget: i64) -> i64 {
    let mut best = vec![0i64; (budget + 1) as usize];
    for i in 0..present.len() {
        let cost = present[i];
        let gain = future[i] - present[i];
        if gain <= 0 {
            continue;
        }
        for b in (cost..budget + 1).rev() {
            best[b as usize] = best[b as usize].max(best[(b - cost) as usize] + gain);
        }
    }
    best[budget as usize]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2291;
    let mut markets: Vec<(Vec<i64>, Vec<i64>)> = Vec::new();
    for _ in 0..100 {
        let mut present = Vec::new();
        let mut future = Vec::new();
        for _ in 0..500 {
            present.push(next_random(&mut seed) % 101);
            future.push(next_random(&mut seed) % 101);
        }
        markets.push((present, future));
    }
    let mut check: i64 = 0;
    for (present, future) in &markets {
        check = (check * 31 + maximum_profit(present, future, 1000)) % 1000000007;
    }
    println!("100 markets of 500 stocks, budget 1000: checksum {}", check);
}
