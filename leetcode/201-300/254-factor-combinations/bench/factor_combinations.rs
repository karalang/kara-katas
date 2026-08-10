// Benchmark workload for LeetCode #254 — Factor Combinations (Rust mirror).
// Mirrors factor_combinations.kara algorithm-for-algorithm: sqrt-bounded
// backtracking under the non-decreasing factor rule, order-independent digest.

fn helper(remaining: i64, start: i64, path: &mut Vec<i64>, out: &mut Vec<Vec<i64>>) {
    let mut i = start;
    while i * i <= remaining {
        if remaining % i == 0 {
            let mut combo = path.clone();
            combo.push(i);
            combo.push(remaining / i);
            out.push(combo);
            path.push(i);
            helper(remaining / i, i, path, out);
            path.pop();
        }
        i += 1;
    }
}

fn main() {
    let hi: i64 = 150000;
    let mut digest: i64 = 0;
    let mut total: i64 = 0;
    for n in 2..=hi {
        let mut out: Vec<Vec<i64>> = Vec::new();
        if n >= 4 {
            let mut path: Vec<i64> = Vec::new();
            helper(n, 2, &mut path, &mut out);
        }
        for c in &out {
            let mut h: i64 = 1;
            for &x in c {
                h = (h * 1000003 + x) % 1000000007;
            }
            digest = (digest + h) % 1000000007;
        }
        total += out.len() as i64;
    }
    println!("{} {}", total, digest);
}
