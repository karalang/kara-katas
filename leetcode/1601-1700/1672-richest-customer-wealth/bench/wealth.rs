// LeetCode #1672: Richest Customer Wealth -- the bench's Rust mirror: the ★
// arm on 4000 grids of 50 customers by 50 banks, up to 100 in each
// account, all drawn first, each answered 100 times.

fn maximum_wealth(accounts: &[Vec<i32>]) -> i32 {
    accounts.iter().map(|row| row.iter().sum()).max().unwrap()
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let grids = 4000;
    let side = 50;
    let rounds: i64 = 100;
    let mut seed: i64 = 1672;
    let mut all: Vec<Vec<Vec<i32>>> = Vec::new();
    for _ in 0..grids {
        let mut accounts: Vec<Vec<i32>> = Vec::new();
        for _ in 0..side {
            let mut row: Vec<i32> = Vec::new();
            for _ in 0..side {
                row.push((next_random(&mut seed) % 100 + 1) as i32);
            }
            accounts.push(row);
        }
        all.push(accounts);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for accounts in &all {
            let richest = maximum_wealth(accounts) as i64;
            total += richest;
            check = (check * 31 + richest + r) % 1000000007;
        }
    }
    println!("{} grids of {} by {}, {} rounds: answers sum to {}, checksum {}", grids, side, side, rounds, total, check);
}
