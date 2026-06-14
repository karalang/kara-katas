// LeetCode #171 — rayon-parallel Rust mirror (par lane).
//
// Same Horner-fold base-26 parse as ../../column_number.rs, but the K_ITERS
// reduction runs across a rayon thread pool via
// `.into_par_iter().map(...).sum()` (the corpus is built once, shared read-only).
// Hand-tuned-parallel comparator for Kāra's auto-par: the Rust programmer adds
// the `rayon` crate and rewrites the loop into a parallel iterator; Kāra
// parallelizes the identical reduction with no source change. Same sink.

use rayon::prelude::*;

const LEN: i64 = 50_000;
const K_ITERS: i64 = 100_000_000;
const LETTERS: &[u8; 26] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ";

fn to_title(mut num: i64) -> String {
    let mut bytes = Vec::new();
    while num > 0 {
        num -= 1;
        bytes.push(LETTERS[(num % 26) as usize]);
        num /= 26;
    }
    bytes.reverse();
    String::from_utf8(bytes).unwrap()
}

fn to_number(title: &str) -> i64 {
    let mut n: i64 = 0;
    for &b in title.as_bytes() {
        n = n * 26 + (b - b'A') as i64 + 1;
    }
    n
}

fn main() {
    let corpus: Vec<String> = (1..=LEN).map(to_title).collect();
    let sum: i64 = (0..K_ITERS)
        .into_par_iter()
        .map(|k| to_number(&corpus[(k % LEN) as usize]))
        .sum();
    println!("{}", sum);
}
