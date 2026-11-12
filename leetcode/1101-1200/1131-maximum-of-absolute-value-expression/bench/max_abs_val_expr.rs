// LeetCode #1131: Maximum of Absolute Value Expression -- the bench in
// Rust, the same algorithm and workload as max_abs_val_expr.kara: each
// array its own `Vec<i64>`, the same 8 pairs of 40000 values and 400
// rounds.

fn max_abs_val_expr(arr1: &[i64], arr2: &[i64]) -> i64 {
    let mut best = 0;
    for &(p, q) in &[(1i64, 1i64), (1, -1), (-1, 1), (-1, -1)] {
        let mut high = i64::MIN;
        let mut low = i64::MAX;
        for i in 0..arr1.len() {
            let v = p * arr1[i] + q * arr2[i] + i as i64;
            high = high.max(v);
            low = low.min(v);
        }
        best = best.max(high - low);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn value(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    let low = next_random(seed);
    (high * 32768 + low) % 2000001 - 1000000
}

fn main() {
    let mut seed = 1131;
    let mut firsts: Vec<Vec<i64>> = Vec::new();
    let mut seconds: Vec<Vec<i64>> = Vec::new();
    for _ in 0..8 {
        let a: Vec<i64> = (0..40000).map(|_| value(&mut seed)).collect();
        let b: Vec<i64> = (0..40000).map(|_| value(&mut seed)).collect();
        firsts.push(a);
        seconds.push(b);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..400i64 {
        for j in 0..8usize {
            let at = ((round * 7919 + j as i64 * 104729) % 40000) as usize;
            firsts[j][at] = ((firsts[j][at] + 1000000) * 7 + 12345) % 2000001 - 1000000;
            seconds[j][at] = ((seconds[j][at] + 1000000) * 11 + 54321) % 2000001 - 1000000;
            let r = max_abs_val_expr(&firsts[j], &seconds[j]);
            total += r;
            check = (check * 31 + r) % 1000000007;
        }
    }
    println!("400 rounds over 8 pairs of 40000 values: answers total {}, checksum {}", total, check);
}
