// LeetCode #22 — rayon-parallel Rust mirror (par lane, backtracking).
// Same owned-snapshot recursive backtracking as ../backtracking.rs; the
// K=150 iter reduction runs across a rayon pool. Hand-tuned-parallel
// comparator for Kāra's default build. Sink matches the kara/rust/c/go
// mirrors (50,388,000).

fn backtrack(cur: String, open: i64, close: i64, n: i64, out: &mut Vec<String>) {
    if close == n {
        out.push(cur);
        return;
    }
    if open < n {
        backtrack(format!("{cur}("), open + 1, close, n, out);
    }
    if close < open {
        backtrack(format!("{cur})"), open, close + 1, n, out);
    }
}

fn generate_parenthesis(n: i64) -> Vec<String> {
    let mut out = Vec::new();
    backtrack(String::new(), 0, 0, n, &mut out);
    out
}

fn main() {
    use rayon::prelude::*;
    let n = 10i64;
    let iters = 150;
    let total: u64 = (0..iters)
        .into_par_iter()
        .map(|_| {
            let combos = generate_parenthesis(n);
            let mut bytes: u64 = 0;
            for c in &combos {
                bytes += c.len() as u64;
            }
            bytes
        })
        .sum();
    println!("{total}"); // 150 * 16796 * 20 = 50,388,000
}
