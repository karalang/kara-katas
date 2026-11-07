// LeetCode #1062: Longest Repeating Substring -- the benchmark, the same
// binary search and rolling hash as lrs.kara.
use std::collections::HashMap;

const MOD: i64 = 1000000007;
const BASE: i64 = 131;

// Whether two starts in `s` hold the same `len` bytes.
fn twice(s: &[u8], len: usize) -> bool {
    if len == 0 {
        return true;
    }
    let mut top = 1;
    for _ in 1..len {
        top = top * BASE % MOD;
    }
    let mut hash = 0;
    let mut seen: HashMap<i64, Vec<usize>> = HashMap::new();
    for i in 0..s.len() {
        if i >= len {
            hash = (hash - s[i - len] as i64 * top % MOD + MOD) % MOD;
        }
        hash = (hash * BASE + s[i] as i64) % MOD;
        if i + 1 >= len {
            let start = i + 1 - len;
            let starts = seen.entry(hash).or_insert_with(Vec::new);
            for &other in starts.iter() {
                if s[other..other + len] == s[start..start + len] {
                    return true;
                }
            }
            starts.push(start);
        }
    }
    false
}

fn longest_repeating(s: &str) -> i64 {
    let bytes = s.as_bytes();
    // twice(lo) and not twice(hi)
    let mut lo = 0;
    let mut hi = bytes.len();
    while hi - lo > 1 {
        let mid = lo + (hi - lo) / 2;
        if twice(bytes, mid) {
            lo = mid;
        } else {
            hi = mid;
        }
    }
    lo as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(n: i64, k: i64, seed: &mut i64) -> String {
    let mut s = String::new();
    for _ in 0..n {
        s.push((b'a' + (next_random(seed) % k) as u8) as char);
    }
    s
}

fn main() {
    // 60 strings of 20000 letters over 2 to 26 of them, built once, then
    // each answered
    let mut seed = 1062;
    let mut words: Vec<String> = Vec::new();
    for w in 0..60 {
        words.push(random_word(20000, 2 + w % 25, &mut seed));
    }
    let mut calls = 0;
    let mut total = 0;
    let mut check = 0;
    for w in words.iter() {
        let answer = longest_repeating(w);
        total += answer;
        check = (check * 31 + answer) % 1000000007;
        calls += 1;
    }
    println!("{} calls: answers sum {}, checksum {}", calls, total, check);
}
