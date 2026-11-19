// LeetCode #1648: Sell Diminishing-Valued Colored Balls -- the bench's Rust
// mirror: the ★ arm on 100 random inventories of 100000 colors with up to
// 10^9 balls each, and an order for up to 10^9 of them, all drawn first.

const MOD: i64 = 1_000_000_007;

fn max_profit(inventory: &[i32], orders: i32) -> i32 {
    let mut counts: Vec<i64> = inventory.iter().map(|&b| b as i64).collect();
    counts.sort();
    counts.reverse();
    counts.push(0);
    let mut orders = orders as i64;
    let mut profit = 0;
    for i in 0..counts.len() - 1 {
        let width = (i + 1) as i64;
        let (high, low) = (counts[i], counts[i + 1]);
        if high == low {
            continue;
        }
        let series = |stop: i64| (high + stop + 1) * (high - stop) / 2 % MOD * width % MOD;
        if width * (high - low) < orders {
            profit = (profit + series(low)) % MOD;
            orders -= width * (high - low);
        } else {
            let rows = orders / width;
            let rest = orders % width;
            profit = (profit + series(high - rows)) % MOD;
            profit = (profit + rest * (high - rows) % MOD) % MOD;
            return profit as i32;
        }
    }
    profit as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1648;
    let mut cases = Vec::new();
    for _ in 0..100 {
        let mut inventory: Vec<i32> = Vec::new();
        for _ in 0..100000 {
            inventory.push(((next_random(&mut seed) * 32768 + next_random(&mut seed)) % 1000000000 + 1) as i32);
        }
        let orders = ((next_random(&mut seed) * 32768 + next_random(&mut seed)) % 1000000000 + 1) as i32;
        cases.push((inventory, orders));
    }
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for (inventory, orders) in &cases {
        let profit = max_profit(inventory, *orders) as i64;
        total += profit;
        check = (check * 31 + profit + 1) % 1000000007;
    }
    println!("100 inventories of 100000 colors: profits sum to {}, checksum {}", total, check);
}
