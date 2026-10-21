// Benchmark for #820: Short Encoding of Words -- the ★ arm (a set of the words).
//
// Mirrors short_encoding.kara: put every word in a set, take out every
// proper suffix of every word, and the words left each cost their length
// and a '#'. The set holds views into the words.

use std::collections::HashSet;

fn minimum_length_encoding(words: &[String]) -> i64 {
    let mut kept: HashSet<&str> = HashSet::new();
    for word in words {
        kept.insert(word.as_str());
    }
    for word in words {
        for k in 1..word.len() {
            kept.remove(&word[k..]);
        }
    }
    let mut total = 0i64;
    for word in &kept {
        total += word.len() as i64 + 1;
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(seed: &mut i64, letters: i64, longest: i64) -> String {
    let mut word = String::new();
    let length = 1 + next_random(seed) % longest;
    for _ in 0..length {
        word.push((b'a' + (next_random(seed) % letters) as u8) as char);
    }
    word
}

fn main() {
    let count = 64usize;
    let rounds = 12000usize;
    let mut seed: i64 = 820;
    let mut lists: Vec<Vec<String>> = Vec::new();
    for _ in 0..count {
        let mut words = Vec::new();
        for _ in 0..2000 {
            words.push(random_word(&mut seed, 5, 7));
        }
        lists.push(words);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let answer = minimum_length_encoding(&lists[round % count]);
        total += answer;
        checksum = (checksum * 131 + answer) % 1000000007;
    }
    println!("{rounds} rounds of {count} lists of 2000 words: total {total}, checksum {checksum}");
}
