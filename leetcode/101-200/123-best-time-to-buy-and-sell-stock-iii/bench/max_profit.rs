//! Benchmark workload — at-most-two-transactions DP, Best Time to Buy and Sell Stock III.
//!
//! Algorithmic mirror of bench/max_profit.kara. See ../README.md § Benchmarks for N / K and the LCG.
//! Serial K-loop (each rep perturbs the opening price by the previous result) so all mirrors run the
//! same single-threaded dependency chain. Kara checks integer overflow by default, so the
//! like-for-like row is `rustc -O -C overflow-checks=on`.

fn max_profit(prices: &[i64]) -> i64 {
    if prices.is_empty() {
        return 0;
    }
    let (mut buy1, mut sell1, mut buy2, mut sell2) = (-prices[0], 0i64, -prices[0], 0i64);
    for i in 1..prices.len() {
        let p = prices[i];
        if -p > buy1 {
            buy1 = -p;
        }
        if buy1 + p > sell1 {
            sell1 = buy1 + p;
        }
        if sell1 - p > buy2 {
            buy2 = sell1 - p;
        }
        if buy2 + p > sell2 {
            sell2 = buy2 + p;
        }
    }
    sell2
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
        let r = max_profit(&data);
        sum += r;
        data[0] = ((data[0] + r) & 4095) + 1;
    }
    println!("{}", sum);
}
