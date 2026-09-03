// Benchmark mirror — LeetCode 309, Best Time to Buy and Sell Stock with Cooldown.
// Same three-state DP, same LCG series, same per-pass perturbation and masked
// sink as cooldown.kara. See ../README.md § Benchmarks.

fn main() {
    let n: i64 = 200000;
    let passes: i64 = 1900;

    let mut prices: Vec<i64> = Vec::with_capacity(n as usize);
    let mut state: i64 = 20309;
    for _ in 0..n {
        state = (state * 1103515245 + 12345) % 2147483648;
        prices.push(state % 2001 - 1000);
    }

    let mut checksum: i64 = 0;
    for p in 0..passes {
        let slot = (p % n) as usize;
        prices[slot] = prices[slot] + (checksum & 1);

        let mut hold = -prices[0];
        let mut sold: i64 = 0;
        let mut rest: i64 = 0;
        for i in 1..n as usize {
            let prev_hold = hold;
            let prev_sold = sold;
            let prev_rest = rest;
            hold = prev_hold;
            if prev_rest - prices[i] > hold {
                hold = prev_rest - prices[i];
            }
            sold = prev_hold + prices[i];
            rest = prev_rest;
            if prev_sold > rest {
                rest = prev_sold;
            }
        }
        let mut best = rest;
        if sold > best {
            best = sold;
        }
        checksum = (checksum + best) & 0x3FFFFFFF;
    }
    println!("checksum {}", checksum);
}
