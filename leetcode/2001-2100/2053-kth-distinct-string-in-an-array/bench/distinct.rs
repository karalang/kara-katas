// LeetCode #2053: Kth Distinct String in an Array -- Rust mirror of the
// ★ arm's benchmark (distinct.kara): the same 5000 arrays, the same count
// into a hash map (std's SipHash `HashMap`, a clone of each string as its
// key) and walk of the array.
use std::collections::HashMap;

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn kth_distinct(arr: &[String], k: i64) -> String {
    let mut counts: HashMap<String, i64> = HashMap::new();
    for s in arr {
        *counts.entry(s.clone()).or_insert(0) += 1;
    }
    let mut left = k;
    for s in arr {
        if counts[s] == 1 {
            left -= 1;
            if left == 0 {
                return s.clone();
            }
        }
    }
    String::new()
}

fn main() {
    let alphabet: Vec<char> = "abcdefghijklmnopqrstuvwxyz".chars().collect();
    let mut seed = 2053i64;
    let (mut found, mut check) = (0i64, 0i64);
    for t in 0..5000i64 {
        let letters = 2 + t % 25;
        let mut arr: Vec<String> = Vec::with_capacity(1000);
        for _ in 0..1000 {
            let len = next_random(&mut seed) % 5 + 1;
            let mut s = String::new();
            for _ in 0..len {
                s.push(alphabet[(next_random(&mut seed) % letters) as usize]);
            }
            arr.push(s);
        }
        let answer = kth_distinct(&arr, t % 1000 + 1);
        if !answer.is_empty() {
            found += 1;
        }
        for ch in answer.chars() {
            check = (check * 31 + ch as i64) % 1000000007;
        }
        check = (check * 31 + answer.len() as i64 + 1) % 1000000007;
    }
    println!("5000 arrays: {} answers found, checksum {}", found, check);
}
