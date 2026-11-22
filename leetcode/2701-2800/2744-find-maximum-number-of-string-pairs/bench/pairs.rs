// LeetCode #2744: Find Maximum Number of String Pairs -- the bench
// (pairs.kara in Rust): a `HashSet<String>` of the words seen.
use std::collections::HashSet;

fn maximum_number_of_string_pairs(words: &[String]) -> i64 {
    let mut seen: HashSet<String> = HashSet::new();
    let mut pairs = 0;
    for w in words.iter() {
        let reversed: String = w.chars().rev().collect();
        if seen.contains(&reversed) {
            pairs += 1;
        }
        seen.insert(w.clone());
    }
    pairs
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 20000;
    let rounds: i64 = 10;
    let mut seed = 2744;
    let mut lists: Vec<Vec<String>> = Vec::new();
    for _ in 0..count {
        let mut words: Vec<String> = Vec::new();
        while words.len() < 50 {
            let a = (b'a' + (next_random(&mut seed) % 8) as u8) as char;
            let b = (b'a' + (next_random(&mut seed) % 8) as u8) as char;
            let w = format!("{}{}", a, b);
            if !words.contains(&w) {
                words.push(w);
            }
        }
        lists.push(words);
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for words in lists.iter() {
            let pairs = maximum_number_of_string_pairs(words);
            sum += pairs;
            check = (check * 31 + pairs + r) % 1000000007;
        }
    }
    println!("{} lists of 50 words, {} rounds: pairs sum to {}, checksum {}", count, rounds, sum, check);
}
