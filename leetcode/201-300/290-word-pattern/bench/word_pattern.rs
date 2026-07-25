// Benchmark harness for LeetCode #290 — Word Pattern.
// Mirrors word_pattern.kara algorithm-for-algorithm.

use std::collections::HashMap;

fn split_words(s: &str) -> Vec<String> {
    let mut words: Vec<String> = Vec::new();
    let mut cur = String::new();
    let mut have = false;
    for b in s.bytes() {
        if b == b' ' {
            if have {
                words.push(std::mem::take(&mut cur));
                have = false;
            }
        } else {
            cur.push(b as char);
            have = true;
        }
    }
    if have {
        words.push(cur);
    }
    words
}

fn word_pattern(pattern: &str, s: &str) -> bool {
    let words = split_words(s);
    let pb = pattern.as_bytes();
    if pb.len() != words.len() {
        return false;
    }

    let mut p2w: HashMap<i64, String> = HashMap::new();
    let mut w2p: HashMap<String, i64> = HashMap::new();

    for i in 0..pb.len() {
        let c = pb[i] as i64;
        let w = &words[i];

        match p2w.get(&c) {
            Some(prev) => {
                if prev != w {
                    return false;
                }
            }
            None => {
                p2w.insert(c, w.clone());
            }
        }
        match w2p.get(w) {
            Some(pc) => {
                if *pc != c {
                    return false;
                }
            }
            None => {
                w2p.insert(w.clone(), c);
            }
        }
    }
    true
}

fn main() {
    let np: i64 = 8;
    let pl: i64 = 1000;
    let alpha_n: i64 = 26;
    let iters: i64 = 2500;

    let alpha: Vec<String> = (0..alpha_n)
        .map(|a| ((97 + a) as u8 as char).to_string())
        .collect();

    let mut patterns: Vec<String> = Vec::new();
    let mut subjects: Vec<String> = Vec::new();
    for j in 0..np {
        let mut pat = String::new();
        let mut sub = String::new();
        for i in 0..pl {
            let slot = (i + j) % alpha_n;
            pat.push_str(&alpha[slot as usize]);
            if i > 0 {
                sub.push(' ');
            }
            let mut wslot = slot;
            if j % 2 == 1 && i == pl - 1 {
                wslot = j % alpha_n;
            }
            sub.push_str(&format!("w{}", wslot));
        }
        patterns.push(pat);
        subjects.push(sub);
    }

    let mut sink: i64 = 0;
    for it in 0..iters {
        let idx = ((it * 3) % np) as usize;
        if word_pattern(&patterns[idx], &subjects[idx]) {
            sink += it + 1;
        } else {
            sink += 1;
        }
    }
    println!("{}", sink);
}
