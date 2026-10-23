// LeetCode #884 bench: Rust mirror of uncommon_from_sentences.kara (the ★
// arm, one map of counts) on the same 1000 sentences.

use std::collections::HashMap;

fn uncommon_from_sentences(s1: &str, s2: &str) -> Vec<String> {
    let mut counts: HashMap<String, i64> = HashMap::new();
    for word in s1.split(' ') {
        let n = counts.get(word).copied().unwrap_or(0);
        counts.insert(word.to_string(), n + 1);
    }
    for word in s2.split(' ') {
        let n = counts.get(word).copied().unwrap_or(0);
        counts.insert(word.to_string(), n + 1);
    }
    let mut out: Vec<String> = Vec::new();
    for (word, n) in counts.iter() {
        if *n == 1 {
            out.push(word.clone());
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

// up to 200 characters, words of 1 to 4 of the letters a to e
fn sentence(seed: &mut i64) -> String {
    let mut out = String::new();
    loop {
        let size = next_random(seed) % 4 + 1;
        let mut word = String::new();
        for _ in 0..size {
            word.push((97 + next_random(seed) % 5) as u8 as char);
        }
        if out.is_empty() {
            out = word;
        } else if out.len() + 1 + word.len() <= 200 {
            out = out + " " + &word;
        } else {
            return out;
        }
        if next_random(seed) % 80 == 0 {
            return out;
        }
    }
}

// the same for a word wherever it sits in the answer
fn word_hash(word: &str) -> i64 {
    let mut h: i64 = 7;
    for &b in word.as_bytes() {
        h = (h * 131 + b as i64) % 1000000007;
    }
    h
}

fn main() {
    let mut seed = 884;
    let sentences: Vec<String> = (0..1000).map(|_| sentence(&mut seed)).collect();
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..200 {
        for i in 0..1000 {
            let words = uncommon_from_sentences(&sentences[i], &sentences[(i + r + 1) % 1000]);
            total += words.len() as i64;
            for w in &words {
                check = (check + word_hash(w)) % 1000000007;
            }
        }
    }
    println!("1000 sentences, each paired with 200 others: {} uncommon words, checksum {}", total, check);
}
