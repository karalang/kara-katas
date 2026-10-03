// Benchmark workload for LeetCode #336 — Rust mirror of palindrome_pairs.kara.
use std::collections::{HashMap, HashSet};

const WORDS: usize = 20000;
const PUNCHES: i64 = 50;
const MODULUS: i64 = 1073741789;

fn is_palindrome(b: &[u8], lo: usize, hi: usize) -> bool {
    if hi == 0 {
        return true;
    }
    let (mut i, mut j) = (lo, hi - 1);
    while i < j {
        if b[i] != b[j] {
            return false;
        }
        i += 1;
        j -= 1;
    }
    true
}

fn reversed(s: &str) -> String {
    s.chars().rev().collect()
}

fn palindrome_pairs(words: &[String]) -> Vec<(i64, i64)> {
    let mut index: HashMap<String, i64> = HashMap::new();
    for (i, w) in words.iter().enumerate() {
        index.insert(reversed(w), i as i64);
    }
    let mut pairs: Vec<(i64, i64)> = Vec::new();
    for (i, w) in words.iter().enumerate() {
        let i = i as i64;
        let b = w.as_bytes();
        let len = b.len();
        for k in 0..=len {
            if is_palindrome(b, k, len) {
                if let Some(&j) = index.get(&w[0..k]) {
                    if j != i {
                        pairs.push((i, j));
                    }
                }
            }
            if k > 0 && is_palindrome(b, 0, k) {
                if let Some(&j) = index.get(&w[k..len]) {
                    if j != i {
                        pairs.push((j, i));
                    }
                }
            }
        }
    }
    pairs.sort();
    pairs
}

fn next(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let alphabet = b"abc";
    let mut seed = 336i64;
    let mut seen: HashSet<String> = HashSet::new();
    let mut words: Vec<String> = Vec::new();
    while words.len() < WORDS {
        let len = 1 + next(&mut seed) % 10;
        let mut w = String::new();
        for _ in 0..len {
            w.push(alphabet[(next(&mut seed) % 3) as usize] as char);
        }
        if !seen.contains(&w) {
            seen.insert(w.clone());
            words.push(w);
        }
    }
    let mut sink = 0i64;
    for _ in 0..PUNCHES {
        let at = (next(&mut seed) % WORDS as i64) as usize;
        let old = words[at].clone();
        words[at].push('d');
        let pairs = palindrome_pairs(&words);
        words[at] = old;
        sink = (sink * 1000003 + pairs.len() as i64) % MODULUS;
        for &(i, j) in &pairs {
            sink = (sink * 31 + i * 7 + j) % MODULUS;
        }
    }
    println!("{sink}");
}
