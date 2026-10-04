// Benchmark mirror of longest_k_distinct.kara (LeetCode #340): a sliding
// window with a count per character in a HashMap. Same strings, rounds and
// sink.
use std::collections::HashMap;

fn longest_k_distinct(s: &str, k: i64) -> i64 {
    let cs: Vec<char> = s.chars().collect();
    let mut counts: HashMap<char, i64> = HashMap::new();
    let mut left = 0usize;
    let mut best = 0i64;
    for right in 0..cs.len() {
        let c = cs[right];
        *counts.entry(c).or_insert(0) += 1;
        while counts.len() as i64 > k {
            let d = cs[left];
            let n = counts[&d] - 1;
            if n == 0 {
                counts.remove(&d);
            } else {
                counts.insert(d, n);
            }
            left += 1;
        }
        best = best.max((right - left + 1) as i64);
    }
    best
}

fn next(state: &mut i64) -> i64 {
    *state = (*state * 1103515245 + 12345) % 2147483648;
    *state >> 8
}

fn gen_text(seed: i64, n: i64, alpha: i64) -> String {
    let letters: Vec<char> = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".chars().collect();
    let mut state = seed;
    let mut out = String::new();
    for _ in 0..n {
        out.push(letters[(next(&mut state) % alpha) as usize]);
    }
    out
}

fn main() {
    let alphas = [4i64, 8, 12, 20, 26, 34, 44, 52];
    let texts: Vec<String> = (0..8).map(|i| gen_text(1000 + i as i64, 20000, alphas[i])).collect();
    let mut h: i64 = 0;
    for r in 0..400i64 {
        let k = (r * 7) % 30 + 1;
        h = (h * 31 + longest_k_distinct(&texts[(r % 8) as usize], k)) % 1000000007;
    }
    println!("{}", h);
}
