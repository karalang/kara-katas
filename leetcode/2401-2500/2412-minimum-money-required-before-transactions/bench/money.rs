// LeetCode #2412: Minimum Money Required Before Transactions -- the bench,
// the ★ arm in Rust: the total loss, and the largest of the losing
// transactions' cashbacks and the gaining ones' costs.

fn minimum_money(transactions: &[(i64, i64)]) -> i64 {
    let mut loss = 0;
    let mut extra = 0;
    for &(cost, cashback) in transactions {
        if cost > cashback {
            loss += cost - cashback;
            extra = extra.max(cashback);
        } else {
            extra = extra.max(cost);
        }
    }
    loss + extra
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2412;
    let mut lists: Vec<Vec<(i64, i64)>> = Vec::new();
    let mut top = 1i64;
    for _ in 0..10 {
        top *= 7;
        let ts: Vec<(i64, i64)> = (0..100000)
            .map(|_| {
                let cost = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % (top + 1);
                (cost, (next_random(&mut seed) * 32768 + next_random(&mut seed)) % (top + 1))
            })
            .collect();
        lists.push(ts);
    }
    let mut check: i64 = 0;
    for p in 0..100 {
        for ts in &lists {
            check = (check * 31 + minimum_money(ts) + p) % 1000000007;
        }
    }
    println!("100 passes over 10 lists of 10^5 transactions: checksum {}", check);
}
