// Benchmark for #527: Rust mirror of the ★ arm (grow clashing prefixes);
// see words_abbreviation.kara. Like the ★ arm, every abbreviation is a
// fresh `String` and each round of growing builds a fresh clash `Vec`.
use std::collections::HashSet;

fn abbreviate(word: &str, k: usize) -> String {
    let n = word.len();
    if k + 2 >= n {
        return word.to_string();
    }
    format!("{}{}{}", &word[..k], n - 1 - k, &word[n - 1..])
}

fn words_abbreviation(words: &[String]) -> Vec<String> {
    let n = words.len();
    let mut prefix = vec![1usize; n];
    let mut abbr: Vec<String> = words.iter().map(|w| abbreviate(w, 1)).collect();
    for i in 0..n {
        loop {
            let mut clash: Vec<usize> = Vec::new();
            for j in i + 1..n {
                if abbr[j] == abbr[i] {
                    clash.push(j);
                }
            }
            if clash.is_empty() {
                break;
            }
            clash.push(i);
            for &j in &clash {
                prefix[j] += 1;
                abbr[j] = abbreviate(&words[j], prefix[j]);
            }
        }
    }
    abbr
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(seed: &mut i64, len: i64, letters: i64) -> String {
    let mut word = String::new();
    for _ in 0..len {
        word.push((97 + next_random(seed) % letters) as u8 as char);
    }
    word
}

fn main() {
    let mut seed: i64 = 527;
    let mut lists: Vec<Vec<String>> = Vec::new();
    for _ in 0..20 {
        let mut seen: HashSet<String> = HashSet::new();
        let mut words: Vec<String> = Vec::new();
        while words.len() < 400 {
            let len = 8 + next_random(&mut seed) % 9;
            let word = random_word(&mut seed, len, 2);
            if !seen.contains(&word) {
                seen.insert(word.clone());
                words.push(word);
            }
        }
        lists.push(words);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..50 {
        for l in 0..lists.len() {
            let abbr = words_abbreviation(&lists[l]);
            for a in &abbr {
                total += a.len() as i64;
                for b in a.bytes() {
                    checksum = (checksum * 31 + b as i64) % 1000000007;
                }
            }
        }
    }
    println!("20 lists of 400 words, 50 rounds: {} letters, checksum {}", total, checksum);
}
