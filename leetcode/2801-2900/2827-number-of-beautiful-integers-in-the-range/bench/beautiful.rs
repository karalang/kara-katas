// LeetCode #2827: Number of Beautiful Integers in the Range -- the
// bench's Rust mirror of the ★ arm: a digit DP up to high less one up to
// low - 1, the free started states memoized in a flat `Vec`.

fn walk(digits: &[i64], pos: usize, diff: i64, rem: i64, tight: bool, started: bool, k: i64, memo: &mut Vec<i64>) -> i64 {
    let n = digits.len();
    if pos == n {
        return if started && diff == 0 && rem == 0 { 1 } else { 0 };
    }
    let key = ((pos as i64 * (2 * n as i64 + 1) + diff + n as i64) * k + rem) as usize;
    if !tight && started && memo[key] >= 0 {
        return memo[key];
    }
    let top = if tight { digits[pos] } else { 9 };
    let mut total = 0;
    for d in 0..=top {
        let now = started || d > 0;
        let next_diff = if now { diff + if d % 2 == 0 { 1 } else { -1 } } else { 0 };
        total += walk(digits, pos + 1, next_diff, (rem * 10 + d) % k, tight && d == top, now, k, memo);
    }
    if !tight && started {
        memo[key] = total;
    }
    total
}

fn count_upto(x: i64, k: i64) -> i64 {
    if x <= 0 {
        return 0;
    }
    let digits: Vec<i64> = x.to_string().bytes().map(|c| (c - b'0') as i64).collect();
    let n = digits.len();
    let mut memo = vec![-1i64; n * (2 * n + 1) * k as usize];
    walk(&digits, 0, 0, 0, true, false, k, &mut memo)
}

fn number_of_beautiful_integers(low: i64, high: i64, k: i64) -> i64 {
    count_upto(high, k) - count_upto(low - 1, k)
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
    let count = 2000;
    let rounds = 5;
    let mut seed = 2827;
    let mut cases: Vec<(i64, i64, i64)> = Vec::new();
    for _ in 0..count {
        let a = wide(&mut seed) % 1000000000 + 1;
        let b = wide(&mut seed) % 1000000000 + 1;
        let k = next_random(&mut seed) % 20 + 1;
        cases.push((a.min(b), a.max(b), k));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for &(low, high, k) in &cases {
            let a = number_of_beautiful_integers(low, high, k);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    println!("{} ranges, {} rounds: {} beautiful, checksum {}", count, rounds, total, check);
}
