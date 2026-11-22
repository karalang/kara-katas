// LeetCode #2707: Extra Characters in a String -- the bench (extra.kara in
// Rust): the fewest extra characters of each suffix, from the end back,
// with the dictionary a `HashSet<String>` asked about every slice.

use std::collections::HashSet;

fn min_extra_char(s: &str, dictionary: &[String]) -> i64 {
    let words: HashSet<String> = dictionary.iter().cloned().collect();
    let n = s.len();
    let mut best = vec![0i64; n + 1];
    for i in (0..n).rev() {
        best[i] = best[i + 1] + 1;
        for j in i + 1..n + 1 {
            if words.contains(&s[i..j]) && best[j] < best[i] {
                best[i] = best[j];
            }
        }
    }
    best[0]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(seed: &mut i64, n: i64) -> String {
    (0..n).map(|_| (b'a' + (next_random(seed) % 3) as u8) as char).collect()
}

fn main() {
    let cases = 10000;
    let rounds = 5;
    let mut seed: i64 = 2707;
    let mut problems: Vec<(String, Vec<String>)> = Vec::new();
    for _ in 0..cases {
        let s = random_word(&mut seed, 50);
        let mut dictionary: Vec<String> = Vec::new();
        for _ in 0..50 {
            let n = next_random(&mut seed) % 5 + 1;
            let word = random_word(&mut seed, n);
            if !dictionary.contains(&word) {
                dictionary.push(word);
            }
        }
        problems.push((s, dictionary));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (s, dictionary) in problems.iter() {
            let extra = min_extra_char(s, dictionary);
            sum += extra;
            check = (check * 31 + extra + r) % 1000000007;
        }
    }
    println!("{} strings of 50 letters against up to 50 words, {} rounds: extra characters sum to {}, checksum {}", cases, rounds, sum, check);
}
