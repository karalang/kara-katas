// LeetCode #1553: Minimum Number of Days to Eat N Oranges -- bench: the ★
// arm (halve or third after the single days, every answer kept in a fresh
// map per call) over 20000 piles of 1 to 2*10^9, drawn once, each asked 3
// times. Rust mirror of
// oranges.kara, with std's HashMap (SipHash-1-3, as Kāra's Map).

use std::collections::HashMap;

fn days(n: i64, memo: &mut HashMap<i64, i64>) -> i64 {
    if n <= 1 {
        return n;
    }
    if let Some(&known) = memo.get(&n) {
        return known;
    }
    let halve = n % 2 + days(n / 2, memo);
    let third = n % 3 + days(n / 3, memo);
    let best = 1 + halve.min(third);
    memo.insert(n, best);
    best
}

fn min_days(n: i64) -> i64 {
    let mut memo = HashMap::new();
    days(n, &mut memo)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1553i64;
    let mut piles = Vec::new();
    for _ in 0..20000 {
        let wide = (next_random(&mut seed) * 32768 + next_random(&mut seed)) * 32768 + next_random(&mut seed);
        piles.push(wide % 2000000000 + 1);
    }
    let mut check = 0i64;
    let mut total = 0i64;
    for _ in 0..3 {
        for &n in &piles {
            let d = min_days(n);
            total += d;
            check = mix(check, d);
        }
    }
    println!("3 passes over 20000 piles of up to 2000000000: {} days, checksum {}", total, check);
}
