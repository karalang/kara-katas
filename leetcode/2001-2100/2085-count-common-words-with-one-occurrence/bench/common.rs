// LeetCode #2085: Count Common Words With One Occurrence -- Rust mirror of
// the ★ arm's benchmark (common.kara): the same 2500 pairs of lists, the
// same count of both into a hash map (std's SipHash `HashMap`, a clone of
// each word as its key) and walk of the first.
use std::collections::HashMap;

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn counts(words: &[String]) -> HashMap<String, i64> {
    let mut seen: HashMap<String, i64> = HashMap::new();
    for w in words {
        *seen.entry(w.clone()).or_insert(0) += 1;
    }
    seen
}

fn count_words(words1: &[String], words2: &[String]) -> i64 {
    let one = counts(words1);
    let two = counts(words2);
    one.iter().filter(|(w, &c)| c == 1 && two.get(*w) == Some(&1)).count() as i64
}

fn random_list(seed: &mut i64, alphabet: &[char], letters: i64) -> Vec<String> {
    let mut words: Vec<String> = Vec::with_capacity(1000);
    for _ in 0..1000 {
        let len = next_random(seed) % 4 + 1;
        let mut w = String::new();
        for _ in 0..len {
            w.push(alphabet[(next_random(seed) % letters) as usize]);
        }
        words.push(w);
    }
    words
}

fn main() {
    let alphabet: Vec<char> = "abcdefghijklmnopqrstuvwxyz".chars().collect();
    let mut seed = 2085i64;
    let (mut total, mut check) = (0i64, 0i64);
    for t in 0..2500i64 {
        let letters = 2 + t % 25;
        let words1 = random_list(&mut seed, &alphabet, letters);
        let words2 = random_list(&mut seed, &alphabet, letters);
        let a = count_words(&words1, &words2);
        total += a;
        check = (check * 31 + a) % 1000000007;
    }
    println!("2500 pairs: sum {}, checksum {}", total, check);
}
