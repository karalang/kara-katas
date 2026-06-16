// LeetCode #14 — rayon-parallel Rust mirror (par lane, vertical LCP).
// Same vertical-scan longest_common_prefix as ../vertical.rs; the K=1M
// reduction runs across a rayon pool. Hand-tuned-parallel comparator for
// Kāra's auto-par. Sink matches the kara/rust/c/go mirrors.

fn prefix_string(s: &str, k: i64) -> String {
    let mut out = String::new();
    let mut i: i64 = 0;
    for c in s.chars() {
        if i >= k {
            break;
        }
        out.push(c);
        i += 1;
    }
    out
}

fn longest_common_prefix(strs: &Vec<String>) -> String {
    let n = strs.len() as i64;
    if n == 0 {
        return String::new();
    }
    let first = strs[0].as_bytes();
    let first_len = first.len() as i64;
    let mut col: i64 = 0;
    while col < first_len {
        let c = first[col as usize];
        let mut s: i64 = 1;
        while s < n {
            let other = strs[s as usize].as_bytes();
            if col >= other.len() as i64 || other[col as usize] != c {
                return prefix_string(&strs[0], col);
            }
            s += 1;
        }
        col += 1;
    }
    prefix_string(&strs[0], first_len)
}

fn nth_letter(n: i64) -> char {
    let alphabet = "abcdefghijklmnopqrstuvwxyz";
    let target = n % 26;
    let mut i: i64 = 0;
    for ch in alphabet.chars() {
        if i == target {
            return ch;
        }
        i += 1;
    }
    'a'
}

fn make_string(prefix_len: i64, suffix_id: i64) -> String {
    let alphabet = "abcdefghijklmnopqrstuvwxyz";
    let mut out = String::new();
    let mut i: i64 = 0;
    for ch in alphabet.chars() {
        if i >= prefix_len {
            break;
        }
        out.push(ch);
        i += 1;
    }
    let sig = nth_letter(suffix_id);
    for _ in 0..6 {
        out.push(sig);
    }
    out
}

fn build_case(prefix_len: i64, count: i64) -> Vec<String> {
    let mut v: Vec<String> = Vec::new();
    let mut s: i64 = 0;
    while s < count {
        v.push(make_string(prefix_len, s));
        s += 1;
    }
    v
}

fn main() {
    use rayon::prelude::*;
    let m_cases: i64 = 8;
    let n_strings: i64 = 16;
    let k_iters: i64 = 1_000_000;
    let prefixes: [i64; 8] = [0, 2, 4, 7, 10, 13, 16, 20];

    let mut sets: Vec<Vec<String>> = Vec::new();
    let mut m: i64 = 0;
    while m < m_cases {
        sets.push(build_case(prefixes[m as usize], n_strings));
        m += 1;
    }

    let sum: i64 = (0..k_iters)
        .into_par_iter()
        .map(|k| {
            let idx = (k % m_cases) as usize;
            longest_common_prefix(&sets[idx]).len() as i64
        })
        .sum();
    println!("{}", sum);
}
