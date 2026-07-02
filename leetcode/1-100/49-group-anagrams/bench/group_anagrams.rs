//! Benchmark workload — sorted-key Group Anagrams (LeetCode #49).
//!
//! Algorithmic mirror of bench/group_anagrams.{kara,py,c} and go-seq/main.go.
//! See ../README.md § Benchmarks for the input shape (N=20_000 words, L=8,
//! G=1_000 classes → 26 distinct anagram groups) and K choice. Sink = K*26 = 1040.

use std::collections::HashMap;

const ALPHABET: &[u8] = b"abcdefghijklmnopqrstuvwxyz";

fn count_groups(words: &[String]) -> i64 {
    let mut index_of: HashMap<String, i64> = HashMap::new();
    let mut groups: i64 = 0;
    for w in words {
        let mut bytes: Vec<u8> = w.as_bytes().to_vec();
        bytes.sort_unstable();
        let key = String::from_utf8(bytes).unwrap();
        index_of.entry(key).or_insert_with(|| {
            let g = groups;
            groups += 1;
            g
        });
    }
    groups
}

fn make_words(n: i64, g: i64, l: i64) -> Vec<String> {
    let mut words: Vec<String> = Vec::with_capacity(n as usize);
    for i in 0..n {
        let grp = i % g;
        let rot = (i / g) % l;
        let seed: Vec<u8> = (0..l)
            .map(|k| ALPHABET[((grp + k) % 26) as usize])
            .collect();
        let mut word = Vec::with_capacity(l as usize);
        word.extend_from_slice(&seed[rot as usize..l as usize]);
        word.extend_from_slice(&seed[0..rot as usize]);
        words.push(String::from_utf8(word).unwrap());
    }
    words
}

fn main() {
    let words = make_words(20000, 1000, 8);
    let mut total: i64 = 0;
    for _ in 0..40 {
        total += count_groups(&words);
    }
    println!("{}", total);
}
