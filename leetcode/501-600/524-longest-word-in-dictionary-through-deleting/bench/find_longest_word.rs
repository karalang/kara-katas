// Benchmark for #524: Rust mirror of the ★ arm (check every word); see
// find_longest_word.kara. Like the ★ arm, every subsequence test collects
// the word's letters into a fresh Vec, and a new best word is cloned.

fn is_subsequence(word: &str, s: &str) -> bool {
    let w: Vec<char> = word.chars().collect();
    let mut i = 0;
    for c in s.chars() {
        if i < w.len() && w[i] == c {
            i += 1;
        }
    }
    i == w.len()
}

fn find_longest_word(s: &str, dictionary: &[String]) -> String {
    let mut best = String::new();
    for word in dictionary {
        if word.len() > best.len() || (word.len() == best.len() && *word < best) {
            if is_subsequence(word, s) {
                best = word.clone();
            }
        }
    }
    best
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

fn random_subsequence(seed: &mut i64, s: &str, keep: i64) -> String {
    let mut word = String::new();
    for c in s.chars() {
        if next_random(seed) % keep == 0 {
            word.push(c);
        }
    }
    if word.is_empty() {
        word.push(s.as_bytes()[0] as char);
    }
    word
}

fn main() {
    let mut seed: i64 = 524;
    let mut texts: Vec<String> = Vec::new();
    let mut dictionaries: Vec<Vec<String>> = Vec::new();
    for _ in 0..20 {
        let letters = 2 + next_random(&mut seed) % 4;
        let s = random_word(&mut seed, 1000, letters);
        let mut dictionary: Vec<String> = Vec::new();
        for _ in 0..1000 {
            if next_random(&mut seed) % 3 == 0 {
                let keep = 2 + next_random(&mut seed) % 30;
                dictionary.push(random_subsequence(&mut seed, &s, keep));
            } else {
                let len = 1 + next_random(&mut seed) % 1000;
                dictionary.push(random_word(&mut seed, len, letters));
            }
        }
        texts.push(s);
        dictionaries.push(dictionary);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..20 {
        for c in 0..texts.len() {
            let answer = find_longest_word(&texts[c], &dictionaries[c]);
            total += answer.len() as i64;
            for b in answer.bytes() {
                checksum = (checksum * 31 + b as i64) % 1000000007;
            }
        }
    }
    println!("20 cases, 20 rounds: total {}, checksum {}", total, checksum);
}
