//! Benchmark workload — one-pass O(n) Best Time to Buy and Sell Stock.
//!
//! Algorithmic mirror of bench/one_pass.kara and bench/one_pass.py. See
//! ../README.md § Benchmarks for the choice of N / K and the
//! deterministic LCG generator.

fn max_profit(prices: &[i64]) -> i64 {
    if prices.is_empty() {
        return 0;
    }
    let mut min_price = prices[0];
    let mut best: i64 = 0;
    for &p in &prices[1..] {
        if p < min_price {
            min_price = p;
        }
        let profit = p - min_price;
        if profit > best {
            best = profit;
        }
    }
    best
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
