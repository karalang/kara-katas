//! Benchmark workload — expand-around-center O(n²) Longest Palindromic
//! Substring.
//!
//! Algorithmic mirror of bench/expand_around_center.kara and
//! bench/expand_around_center.py. See ../README.md § Benchmarks for the input
//! shape and K choice.

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

    let mut sum: i64 = 0;
    for _ in 0..10 {
        let (start, length) = longest_palindrome(&data);
        sum += start + length;
    }
    println!("{}", sum);
}
