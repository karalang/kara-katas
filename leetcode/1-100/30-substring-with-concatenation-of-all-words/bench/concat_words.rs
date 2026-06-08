// Benchmark workload — substring-with-concatenation, LeetCode #30 (sliding window).
//
// Algorithmic mirror of concat_words.kara, compiled with `rustc -O`. Same
// 16-word vocabulary, same glibc LCG (high bits for the vocab pick), same
// NSLOTS / RUNS, same O(n) sliding-window search, same sink. Keys are `&str`
// slices into the text (no per-piece allocation) — the idiomatic Rust shape.

use std::collections::HashMap;

fn find_substring(s: &str, words: &[&str]) -> Vec<i64> {
    let mut result: Vec<i64> = Vec::new();
    let k = words.len();
    if k == 0 {
        return result;
    }
    let wl = words[0].len();
    let total = wl * k;
    let n = s.len();
    if wl == 0 || total > n {
        return result;
    }

    let mut need: HashMap<&str, i64> = HashMap::new();
    for w in words {
        *need.entry(w).or_insert(0) += 1;
    }

    for r in 0..wl {
        let mut seen: HashMap<&str, i64> = HashMap::new();
        let mut count: i64 = 0;
        let mut left = r;
        let mut j = r;
        while j + wl <= n {
            let piece = &s[j..j + wl];
            match need.get(piece) {
                None => {
                    seen.clear();
                    count = 0;
                    left = j + wl;
                }
                Some(&req) => {
                    *seen.entry(piece).or_insert(0) += 1;
                    count += 1;
                    while *seen.get(piece).unwrap_or(&0) > req {
                        let lw = &s[left..left + wl];
                        *seen.entry(lw).or_insert(0) -= 1;
                        left += wl;
                        count -= 1;
                    }
                    if count == k as i64 {
                        result.push(left as i64);
                        let lw = &s[left..left + wl];
                        *seen.entry(lw).or_insert(0) -= 1;
                        left += wl;
                        count -= 1;
                    }
                }
            }
            j += wl;
        }
    }
    result
}

fn main() {
    let nslots: i64 = 50000;
    let runs: i64 = 40;

    let chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/";
    let vocab: Vec<&str> = (0..16).map(|v| &chars[v * 4..v * 4 + 4]).collect();

    let mut s = String::new();
    let mut state: i64 = 1;
    for _ in 0..nslots {
        state = (state * 1103515245 + 12345) % 2147483648;
        let v = ((state / 131072) % 16) as usize;
        s.push_str(vocab[v]);
    }

    let mut sink: i64 = 0;
    for run in 0..runs {
        let start = (run % 13) as usize;
        let words_r: Vec<&str> = (0..4).map(|d| vocab[start + d]).collect();
        let res = find_substring(&s, &words_r);
        sink += res.len() as i64;
        for idx in &res {
            sink += idx;
        }
    }

    println!("{}", sink);
}
