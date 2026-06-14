// LeetCode #125 — rayon-parallel Rust mirror (par lane).
//
// Same allocating filter-then-compare as ../valid_palindrome.rs, but the ITERS
// reduction runs across a rayon thread pool via `.into_par_iter().map().sum()`.
// Hand-tuned-parallel comparator for Kāra's auto-par: the Rust programmer adds
// the `rayon` crate and rewrites the loop into a parallel iterator; Kāra
// parallelizes the identical `sum += pass(...)` reduction with no source
// change. Same sink (3000000) as every other mirror.

use rayon::prelude::*;

const ITERS: i64 = 3_000_000;

fn is_alnum(b: u8) -> bool {
    b.is_ascii_digit() || b.is_ascii_lowercase() || b.is_ascii_uppercase()
}

fn is_palindrome(s: &[u8]) -> bool {
    let mut clean: Vec<u8> = Vec::new();
    for &b in s {
        if is_alnum(b) {
            clean.push(b.to_ascii_lowercase());
        }
    }
    let m = clean.len();
    if m == 0 {
        return true;
    }
    let (mut lo, mut hi) = (0usize, m - 1);
    while lo < hi {
        if clean[lo] != clean[hi] {
            return false;
        }
        lo += 1;
        hi -= 1;
    }
    true
}

fn main() {
    let input = "A man, a plan, a canal: Panama".repeat(8);
    let bytes = input.as_bytes();
    let sum: i64 = (0..ITERS)
        .into_par_iter()
        .map(|_| is_palindrome(bytes) as i64)
        .sum();
    println!("{}", sum);
}
