// LeetCode #5 — rayon-parallel Rust mirror (par lane, expand_around_center).
// Same O(n²) expand-around-center longest_palindrome as ../expand_around_center.rs;
// the K=100-call reduction runs across a rayon pool. Hand-tuned-parallel
// comparator for Kāra's auto-par (which parallelizes the same K-loop from zero
// parallel source). Sink = 500000 (K=100 × (best_start 0 + best_len 5000)).
// longest_palindrome allocates a Vec<char> per call, so it is not hoisted out of
// the loop — no black_box needed (the seq lane doesn't use one either).
use rayon::prelude::*;

fn expand(chars: &[char], lo0: i64, hi0: i64) -> (i64, i64) {
    let mut lo = lo0;
    let mut hi = hi0;
    let n = chars.len() as i64;
    while lo >= 0 && hi < n && chars[lo as usize] == chars[hi as usize] {
        lo -= 1;
        hi += 1;
    }
    (lo + 1, hi - lo - 1)
}

fn longest_palindrome(s: &str) -> (i64, i64) {
    let chars: Vec<char> = s.chars().collect();
    let n = chars.len() as i64;
    let mut best_start: i64 = 0;
    let mut best_len: i64 = 0;
    let mut i: i64 = 0;
    while i < n {
        let (start, length) = expand(&chars, i, i);
        if length > best_len {
            best_start = start;
            best_len = length;
        }
        let (start, length) = expand(&chars, i, i + 1);
        if length > best_len {
            best_start = start;
            best_len = length;
        }
        i += 1;
    }
    (best_start, best_len)
}

fn main() {
    let data: String = "a".repeat(5000);

    let sum: i64 = (0..100)
        .into_par_iter()
        .map(|_| {
            let (start, length) = longest_palindrome(&data);
            start + length
        })
        .sum();
    println!("{}", sum);
}
