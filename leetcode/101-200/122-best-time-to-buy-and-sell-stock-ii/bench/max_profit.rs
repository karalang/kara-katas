//! Benchmark workload — greedy O(n) Best Time to Buy and Sell Stock II.
//!
//! Algorithmic mirror of bench/max_profit.kara and bench/max_profit.py. See
//! ../README.md § Benchmarks for the choice of N / K and the deterministic LCG
//! generator. Kara checks integer overflow by default, so the like-for-like row
//! is `rustc -O -C overflow-checks=on`.

fn max_profit(prices: &[i64]) -> i64 {
    let mut profit: i64 = 0;
    for i in 1..prices.len() {
        let d = prices[i] - prices[i - 1];
        if d > 0 {
            profit += d;
        }
    }
    profit
}

fn main() {
    const N: usize = 2_000_000;
    let mut data: Vec<i64> = Vec::with_capacity(N);
    let mut state: i64 = 12345;
    for _ in 0..N {
        state = (state.wrapping_mul(1103515245).wrapping_add(12345)) & 2_147_483_647;
        data.push((state & 4095) + 1);
    }

    let mut sum: i64 = 0;
    for _ in 0..10 {
        sum += max_profit(&data);
    }
    println!("{}", sum);
}
