// LeetCode #2062: Count Vowel Substrings of a String -- Rust mirror of the
// ★ arm's benchmark (vowels.kara): 20000 words of 100 letters, each a vowel
// with chance 90 in 100, else one of `xyz`; the vowels met from each start
// in a `HashSet<char>`.
use std::collections::HashSet;

fn is_vowel(c: char) -> bool {
    "aeiou".contains(c)
}

fn count_vowel_substrings(word: &str) -> i64 {
    let letters: Vec<char> = word.chars().collect();
    let mut count = 0;
    for i in 0..letters.len() {
        let mut met: HashSet<char> = HashSet::new();
        for j in i..letters.len() {
            if !is_vowel(letters[j]) {
                break;
            }
            met.insert(letters[j]);
            if met.len() == 5 {
                count += 1;
            }
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn word_of(n: i64, p: i64, seed: &mut i64) -> String {
    let vowels: Vec<char> = "aeiou".chars().collect();
    let others: Vec<char> = "xyz".chars().collect();
    let mut out = String::new();
    for _ in 0..n {
        if next_random(seed) % 100 < p {
            out.push(vowels[(next_random(seed) % 5) as usize]);
        } else {
            out.push(others[(next_random(seed) % 3) as usize]);
        }
    }
    out
}

fn main() {
    let mut seed = 2062i64;
    let mut total = 0i64;
    let mut check = 0i64;
    for _ in 0..20000 {
        let a = count_vowel_substrings(&word_of(100, 90, &mut seed));
        total += a;
        check = (check * 31 + a) % 1000000007;
    }
    println!("20000 words: sum {}, checksum {}", total, check);
}
