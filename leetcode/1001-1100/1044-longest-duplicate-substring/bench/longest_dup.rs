// LeetCode #1044: Longest Duplicate Substring -- bench, Rust mirror of
// longest_dup.kara (binary search on the length, rolling hash).

use std::collections::HashMap;

const BASE: i64 = 131;
const MODULUS: i64 = 1_000_000_007;

fn longest_dup_substring(s: &str) -> String {
    let bytes = s.as_bytes();
    let mut low: i64 = 1;
    let mut high: i64 = bytes.len() as i64 - 1;
    let mut best_start = 0usize;
    let mut best_len = 0usize;
    while low <= high {
        let len = (low + high) / 2;
        match repeated_window(bytes, len as usize) {
            Some(start) => {
                best_start = start;
                best_len = len as usize;
                low = len + 1;
            }
            None => high = len - 1,
        }
    }
    s[best_start..best_start + best_len].to_string()
}

fn repeated_window(bytes: &[u8], len: usize) -> Option<usize> {
    let n = bytes.len();
    let mut lead: i64 = 1;
    for _ in 1..len {
        lead = lead * BASE % MODULUS;
    }
    let mut hash: i64 = 0;
    for i in 0..len {
        hash = (hash * BASE + bytes[i] as i64) % MODULUS;
    }
    let mut seen: HashMap<i64, Vec<usize>> = HashMap::new();
    let mut found: Option<usize> = None;
    let mut start = 0;
    loop {
        let earlier = match seen.get(&hash) {
            Some(starts) => starts.iter().any(|&j| same(bytes, j, start, len)),
            None => false,
        };
        if earlier {
            found = match found {
                Some(f) if !smaller(bytes, start, f, len) => Some(f),
                _ => Some(start),
            };
        } else {
            seen.entry(hash).or_insert_with(Vec::new).push(start);
        }
        if start + len == n {
            break;
        }
        hash = (hash - bytes[start] as i64 * lead % MODULUS + MODULUS) % MODULUS;
        hash = (hash * BASE + bytes[start + len] as i64) % MODULUS;
        start += 1;
    }
    found
}

fn same(bytes: &[u8], a: usize, b: usize, len: usize) -> bool {
    for k in 0..len {
        if bytes[a + k] != bytes[b + k] {
            return false;
        }
    }
    true
}

fn smaller(bytes: &[u8], a: usize, b: usize, len: usize) -> bool {
    for k in 0..len {
        if bytes[a + k] != bytes[b + k] {
            return bytes[a + k] < bytes[b + k];
        }
    }
    false
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 12;
    let n: i64 = 30000;
    let rounds = 2;
    let mut seed: i64 = 1044;
    let mut strings: Vec<String> = Vec::new();
    for c in 0..count {
        let k = [2, 4, 8, 26][c % 4];
        let mut letters: Vec<u8> = Vec::new();
        for _ in 0..n {
            letters.push(b'a' + (next_random(&mut seed) % k) as u8);
        }
        if c % 2 == 1 {
            let from = next_random(&mut seed) % (n / 2);
            let to = n / 2 + next_random(&mut seed) % (n / 2 - n / 8);
            for i in 0..n / 8 {
                letters[(to + i) as usize] = letters[(from + i) as usize];
            }
        }
        strings.push(String::from_utf8(letters).unwrap());
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        for s in &strings {
            let answer = longest_dup_substring(s);
            total += answer.len() as i64;
            check = (check * 131 + answer.len() as i64 + 1) % 1000000007;
            for &b in answer.as_bytes() {
                check = (check * 131 + b as i64) % 1000000007;
            }
        }
    }
    println!("{} strings of {} letters, {} rounds: total length {}, checksum {}", count, n, rounds, total, check);
}
