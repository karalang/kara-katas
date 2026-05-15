//! Benchmark workload — sliding-window O(n) Longest Substring Without
//! Repeating Characters.
//!
//! Algorithmic mirror of bench/sliding_window.kara and bench/sliding_window.py.
//! See ../README.md § Benchmarks for the input shape and K choice.

use std::collections::HashMap;

fn length_of_longest_substring(s: &str) -> i64 {
    let mut last_idx: HashMap<char, i64> = HashMap::new();
    let mut left: i64 = 0;
    let mut best: i64 = 0;
    for (right, c) in s.chars().enumerate() {
        let right = right as i64;
        if let Some(&prev) = last_idx.get(&c) {
            if prev >= left {
                left = prev + 1;
            }
        }
        last_idx.insert(c, right);
        let window = right - left + 1;
        if window > best {
            best = window;
        }
    }
    best
}

fn main() {
    let data: String = "abcdefghijklmnopqrstuvwxyz".repeat(4000); // 104_000 chars

    let mut sum: i64 = 0;
    for _ in 0..20 {
        sum += length_of_longest_substring(&data);
    }
    println!("{}", sum);
}
