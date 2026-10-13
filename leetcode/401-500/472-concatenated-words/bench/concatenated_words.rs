// Benchmark for #472 -- Rust mirror of the ★ arm (concatenated_words.kara):
// shortest first, each word broken against the words before it.
use std::collections::HashSet;

fn breaks(word: &str, known: &HashSet<String>) -> bool {
    let n = word.len();
    let mut reach = vec![false; n + 1];
    reach[0] = true;
    for end in 1..=n {
        for start in 0..end {
            if reach[start] && known.contains(&word[start..end]) {
                reach[end] = true;
                break;
            }
        }
    }
    reach[n]
}

fn find_all_concatenated_words_in_a_dict(words: &[String]) -> Vec<String> {
    let mut order = words.to_vec();
    order.sort_by_key(|w| w.len());
    let mut known: HashSet<String> = HashSet::new();
    let mut found = Vec::new();
    for word in &order {
        if !known.is_empty() && breaks(word, &known) {
            found.push(word.clone());
        }
        known.insert(word.clone());
    }
    found
}

// ---- bench ------------------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let size = 10000;
    let mut seed: i64 = 472;
    let mut seen: HashSet<String> = HashSet::new();
    let mut words: Vec<String> = Vec::new();
    while words.len() < size {
        let mut w = String::new();
        if words.len() < 1000 {
            let letters = 2 + next_random(&mut seed) % 4;
            for _ in 0..letters {
                w.push((97 + next_random(&mut seed) % 4) as u8 as char);
            }
        } else {
            let parts = 2 + next_random(&mut seed) % 2;
            for _ in 0..parts {
                let i = (next_random(&mut seed) % words.len() as i64) as usize;
                let piece = words[i].clone();
                w.push_str(&piece);
            }
            if next_random(&mut seed) % 4 == 0 {
                w.push('e');
            }
        }
        if w.len() <= 30 && !seen.contains(&w) {
            seen.insert(w.clone());
            words.push(w);
        }
    }
    let rounds = 10;
    let mut found = 0;
    let mut hash_sum: i64 = 0;
    for _ in 0..rounds {
        let got = find_all_concatenated_words_in_a_dict(&words);
        found += got.len();
        for w in &got {
            let mut h: i64 = 0;
            for b in w.bytes() {
                h = (h * 31 + b as i64) % 1000000007;
            }
            hash_sum = (hash_sum + h) % 1000000007;
        }
    }
    println!("{rounds} rounds on {size} words: {found} concatenated, hash sum {hash_sum}");
}
