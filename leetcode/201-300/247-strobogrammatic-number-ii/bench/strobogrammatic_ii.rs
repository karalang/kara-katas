// Benchmark workload for LeetCode #247 — Strobogrammatic Number II (Rust mirror).
// Mirrors strobogrammatic_ii.kara algorithm-for-algorithm.

const PAIR_A: [&str; 5] = ["0", "1", "6", "8", "9"];
const PAIR_B: [&str; 5] = ["0", "1", "9", "8", "6"];

fn build(k: i64, n: i64) -> Vec<String> {
    let mut out: Vec<String> = Vec::new();
    if k == 0 {
        out.push(String::new());
        return out;
    }
    if k == 1 {
        out.push("0".to_string());
        out.push("1".to_string());
        out.push("8".to_string());
        return out;
    }
    let inner = build(k - 2, n);
    for s in &inner {
        for p in 0..5 {
            if k == n && PAIR_A[p] == "0" {
                continue;
            }
            let mut t = String::new();
            t.push_str(PAIR_A[p]);
            t.push_str(s);
            t.push_str(PAIR_B[p]);
            out.push(t);
        }
    }
    out
}

fn is_strobogrammatic(s: &str) -> bool {
    let b = s.as_bytes();
    if b.is_empty() {
        return true;
    }
    let (mut lo, mut hi) = (0i64, b.len() as i64 - 1);
    while lo <= hi {
        let x = b[lo as usize] as i64;
        let y = b[hi as usize] as i64;
        let ok = (x == 48 && y == 48) || (x == 49 && y == 49) || (x == 56 && y == 56)
            || (x == 54 && y == 57) || (x == 57 && y == 54);
        if !ok {
            return false;
        }
        lo += 1;
        hi -= 1;
    }
    true
}

fn main() {
    let n: i64 = 16;
    let rounds: i64 = 12;
    let mut sink: i64 = 0;
    for _ in 0..rounds {
        let got = build(n, n);
        for s in &got {
            if is_strobogrammatic(s) {
                for &c in s.as_bytes() {
                    sink = (sink * 31 + c as i64) % 1000000007;
                }
            }
        }
    }
    println!("{}", sink);
}
