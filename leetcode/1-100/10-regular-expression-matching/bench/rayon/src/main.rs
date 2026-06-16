// LeetCode #10 — rayon-parallel Rust mirror (par lane, regex).
// Same recursive is_match_at as ../regex.rs; the K=10M reduction runs
// across a rayon pool. Hand-tuned-parallel comparator for Kāra's auto-par.
// Sink matches the kara/rust/c/go mirrors.

fn is_match_at(s: &[u8], i: usize, p: &[u8], j: usize) -> bool {
    let n = s.len();
    let m = p.len();

    if j == m {
        return i == n;
    }

    let first_match = i < n && (p[j] == s[i] || p[j] == b'.');

    if j + 1 < m && p[j + 1] == b'*' {
        return is_match_at(s, i, p, j + 2)
            || (first_match && is_match_at(s, i + 1, p, j));
    }

    first_match && is_match_at(s, i + 1, p, j + 1)
}

fn is_match(s: &str, p: &str) -> bool {
    is_match_at(s.as_bytes(), 0, p.as_bytes(), 0)
}

fn main() {
    use rayon::prelude::*;
    let n: i64 = 8;
    let k_iters: i64 = 10_000_000;

    let strs: Vec<&str> = vec![
        "aa",
        "ab",
        "aab",
        "mississippi",
        "aaaaaaaaaab",
        "aaa",
        "abc",
        "aaab",
    ];
    let pats: Vec<&str> = vec![
        "a*",
        ".*",
        "c*a*b",
        "mis*is*p*.",
        "a*a*a*a*a*b",
        "ab*a",
        "...",
        "a*b",
    ];

    let sum: i64 = (0..k_iters)
        .into_par_iter()
        .map(|k| {
            let idx = (k % n) as usize;
            if is_match(strs[idx], pats[idx]) {
                1
            } else {
                0
            }
        })
        .sum();
    println!("{}", sum);
}
