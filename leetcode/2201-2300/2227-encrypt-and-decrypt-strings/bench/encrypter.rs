// LeetCode #2227: Encrypt and Decrypt Strings -- the benchmark's Rust
// mirror of encrypter.kara: a `HashMap` of values and a `HashMap`
// counting the dictionary's encryptions.

use std::collections::HashMap;

struct Encrypter {
    table: HashMap<char, String>,
    counts: HashMap<String, i64>,
}

impl Encrypter {
    fn new(keys: &[char], values: &[String], dictionary: &[String]) -> Encrypter {
        let mut table = HashMap::new();
        for i in 0..keys.len() {
            table.insert(keys[i], values[i].clone());
        }
        let mut encrypter = Encrypter { table, counts: HashMap::new() };
        for word in dictionary {
            let secret = encrypter.encrypt(word);
            if !secret.is_empty() {
                *encrypter.counts.entry(secret).or_insert(0) += 1;
            }
        }
        encrypter
    }

    fn encrypt(&self, word1: &str) -> String {
        let mut secret = String::new();
        for c in word1.chars() {
            match self.table.get(&c) {
                Some(value) => secret.push_str(value),
                None => return String::new(),
            }
        }
        secret
    }

    fn decrypt(&self, word2: &str) -> i64 {
        *self.counts.get(word2).unwrap_or(&0)
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn draw_word(seed: &mut i64, length: i64, letters: i64) -> String {
    (0..length).map(|_| (97 + next_random(seed) % letters) as u8 as char).collect()
}

fn main() {
    let mut seed = 2227;
    let mut keys = Vec::new();
    let mut values = Vec::new();
    for i in 0..26 {
        keys.push((97 + i) as u8 as char);
        values.push(draw_word(&mut seed, 2, 3));
    }
    let mut dictionary: Vec<String> = (0..100).map(|_| draw_word(&mut seed, 100, 26)).collect();
    let mut words = Vec::new();
    for i in 0..200 {
        if i % 2 == 0 {
            let length = next_random(&mut seed) % 2000 + 1;
            words.push(draw_word(&mut seed, length, 26));
        } else if i % 4 == 1 {
            let at = (next_random(&mut seed) % 100) as usize;
            words.push(dictionary[at].chars().map(|c| values[(c as u8 - 97) as usize].as_str()).collect());
        } else {
            words.push(draw_word(&mut seed, 200, 3));
        }
    }
    let mut check: i64 = 0;
    for _ in 0..500 {
        // punch: one dictionary word drawn again before each round
        let at = (next_random(&mut seed) % 100) as usize;
        dictionary[at] = draw_word(&mut seed, 100, 26);
        let encrypter = Encrypter::new(&keys, &values, &dictionary);
        for i in 0..200 {
            if i % 2 == 0 {
                let secret = encrypter.encrypt(&words[i]);
                check = (check * 31 + secret.len() as i64 + secret.as_bytes()[secret.len() / 2] as i64) % 1000000007;
            } else {
                check = (check * 31 + encrypter.decrypt(&words[i])) % 1000000007;
            }
        }
    }
    println!("500 rounds of 200 calls: checksum {check}");
}
