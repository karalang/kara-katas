// Benchmark for #819: Most Common Word -- the ★ arm (a map of counts).
//
// Mirrors most_common_word.kara: lower every letter and turn everything
// else into a space, count each word that is not banned in a map, and
// return the word counted most, the first alphabetically of two counted
// as often.

use std::collections::{HashMap, HashSet};

fn most_common_word(paragraph: &str, banned: &[String]) -> String {
    let cleaned: String = paragraph
        .chars()
        .map(|c| if c.is_ascii_alphabetic() { c.to_ascii_lowercase() } else { ' ' })
        .collect();
    let ruled_out: HashSet<&str> = banned.iter().map(|w| w.as_str()).collect();
    let mut counts: HashMap<&str, i64> = HashMap::new();
    for word in cleaned.split_whitespace() {
        if !ruled_out.contains(word) {
            *counts.entry(word).or_insert(0) += 1;
        }
    }
    let mut best = "";
    let mut most = 0;
    for (word, n) in counts.iter() {
        if *n > most || (*n == most && *word < best) {
            best = word;
            most = *n;
        }
    }
    best.to_string()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(seed: &mut i64) -> String {
    let length = 1 + next_random(seed) % 10;
    let mut word = String::new();
    for _ in 0..length {
        word.push((b'a' + (next_random(seed) % 26) as u8) as char);
    }
    word
}

fn main() {
    let count = 64;
    let rounds: i64 = 200000;
    let mut seed: i64 = 819;
    let marks = [" ", " ", " ", ", ", ". ", "! ", "? ", "; ", "' ", ","];
    let vocabulary: Vec<String> = (0..300).map(|_| random_word(&mut seed)).collect();
    let mut paragraphs: Vec<String> = Vec::new();
    let mut banned: Vec<Vec<String>> = Vec::new();
    for _ in 0..count {
        let mut paragraph = String::new();
        while paragraph.len() < 990 {
            let a = next_random(&mut seed) % 300;
            let k = (a * (next_random(&mut seed) % 300) / 300) as usize;
            let mut word = vocabulary[k].clone();
            if next_random(&mut seed) % 4 == 0 {
                word = word.to_uppercase();
            }
            paragraph.push_str(&word);
            paragraph.push_str(marks[(next_random(&mut seed) % 10) as usize]);
        }
        paragraphs.push(paragraph);
        let mut ruled_out: Vec<String> = Vec::new();
        for _ in 0..50 {
            ruled_out.push(vocabulary[(next_random(&mut seed) % 30) as usize].clone());
        }
        for _ in 0..50 {
            ruled_out.push(random_word(&mut seed));
        }
        banned.push(ruled_out);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let g = (round % count as i64) as usize;
        let answer = most_common_word(&paragraphs[g], &banned[g]);
        total += answer.len() as i64;
        for b in answer.bytes() {
            checksum = (checksum * 131 + b as i64) % 1000000007;
        }
    }
    println!("{} rounds of {} paragraphs: total {}, checksum {}", rounds, count, total, checksum);
}
