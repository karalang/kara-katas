// Benchmark workload for LeetCode #350 — Rust mirror of intersect.kara.
// std's HashMap hashes with SipHash-1-3 under a random key, as Kara's Map does.
use std::collections::HashMap;

const POOL: i64 = 1000000;
const LEN: i64 = 1000;
const PAIRS: i64 = 20000;

fn intersect(a: &[i64], b: &[i64]) -> Vec<i64> {
    let mut counts: HashMap<i64, i64> = HashMap::new();
    for &x in a {
        *counts.entry(x).or_insert(0) += 1;
    }
    let mut out: Vec<i64> = Vec::new();
    for &y in b {
        let left = *counts.get(&y).unwrap_or(&0);
        if left > 0 {
            counts.insert(y, left - 1);
            out.push(y);
        }
    }
    out.sort();
    out
}

fn main() {
    let mut pool: Vec<i64> = Vec::new();
    let mut x: i64 = 350;
    for _ in 0..POOL {
        x = (x * 1103515245 + 12345) % 2147483648;
        pool.push(x / 16 % 1001);
    }

    let mut sink: i64 = 0;
    for _ in 0..PAIRS {
        x = (x * 1103515245 + 12345) % 2147483648;
        let i = (x / 16 % (POOL - LEN)) as usize;
        x = (x * 1103515245 + 12345) % 2147483648;
        let j = (x / 16 % (POOL - LEN)) as usize;
        let a = pool[i..i + LEN as usize].to_vec();
        let b = pool[j..j + LEN as usize].to_vec();
        let r = intersect(&a, &b);
        let s: i64 = r.iter().sum();
        sink = (sink * 31 + r.len() as i64 * 1000003 + s) % 1000000007;
    }
    println!("sink {}", sink);
}
