// Benchmark for #425: mirror of word_squares.kara (a map of prefixes).
use std::collections::{HashMap, HashSet};

fn extend(rows: &mut Vec<String>, length: usize, by_prefix: &HashMap<String, Vec<usize>>, words: &[String], found: &mut Vec<Vec<String>>) {
    let r = rows.len();
    if r == length {
        found.push(rows.clone());
        return;
    }
    let mut prefix = String::new();
    for row in rows.iter() {
        prefix.push(row.as_bytes()[r] as char);
    }
    if let Some(candidates) = by_prefix.get(&prefix) {
        for &i in candidates {
            rows.push(words[i].clone());
            extend(rows, length, by_prefix, words, found);
            rows.pop();
        }
    }
}

fn word_squares(words: &[String]) -> Vec<Vec<String>> {
    let length = words[0].len();
    let mut by_prefix: HashMap<String, Vec<usize>> = HashMap::new();
    for (i, word) in words.iter().enumerate() {
        let bytes = word.as_bytes();
        let mut prefix = String::new();
        for k in 0..length {
            by_prefix.entry(prefix.clone()).or_insert_with(Vec::new).push(i);
            prefix.push(bytes[k] as char);
        }
    }
    let mut found = Vec::new();
    let mut rows = Vec::new();
    extend(&mut rows, length, &by_prefix, words, &mut found);
    found
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(seed: &mut i64) -> String {
    let mut word = String::new();
    for _ in 0..4 {
        word.push((b'a' + (step(seed) % 16) as u8) as char);
    }
    word
}

fn main() {
    let rounds: i64 = std::env::args().nth(1).map_or(20, |s| s.parse().unwrap());
    let n: i64 = 1000;
    let mut seed: i64 = 425;
    let mut seen: HashSet<String> = HashSet::new();
    let mut words: Vec<String> = Vec::new();
    while (words.len() as i64) < n {
        let word = random_word(&mut seed);
        if !seen.contains(&word) {
            seen.insert(word.clone());
            words.push(word);
        }
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        let mut word = random_word(&mut seed);
        while seen.contains(&word) {
            word = random_word(&mut seed);
        }
        let at = (r * 389 % n) as usize;
        seen.remove(&words[at]);
        seen.insert(word.clone());
        words[at] = word;
        let squares = word_squares(&words);
        total += squares.len() as i64;
        for square in &squares {
            checksum = (checksum * 31 + square[0].as_bytes()[0] as i64 + square[3].as_bytes()[3] as i64) % 1000000007;
        }
    }
    println!("{rounds} rounds on {n} words: {total} squares, checksum {checksum}");
}
