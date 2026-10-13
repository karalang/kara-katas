// Benchmark for #520: Rust mirror of the ★ arm (count the capitals);
// see detect_capital_use.kara.

fn detect_capital_use(word: &str) -> bool {
    let capitals = word.chars().filter(|c| c.is_ascii_uppercase()).count();
    capitals == 0 || capitals == word.len() || (capitals == 1 && word.chars().next().unwrap().is_ascii_uppercase())
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

// A random word of 1 to 100 letters: all capitals, all lower case, a
// capital then lower case, any mix, or one of the first three with one
// letter's case turned.
fn random_word(seed: &mut i64) -> String {
    let len = 1 + next_random(seed) % 100;
    let kind = next_random(seed) % 5;
    let shape = if kind == 4 { next_random(seed) % 3 } else { kind };
    let mut letters: Vec<char> = Vec::new();
    for i in 0..len {
        let c = (97 + next_random(seed) % 26) as u8 as char;
        let capital = if shape == 0 {
            true
        } else if shape == 1 {
            false
        } else if shape == 2 {
            i == 0
        } else {
            next_random(seed) % 2 == 0
        };
        letters.push(if capital { c.to_ascii_uppercase() } else { c });
    }
    if kind == 4 {
        let at = (next_random(seed) % len) as usize;
        letters[at] = if letters[at].is_ascii_uppercase() { letters[at].to_ascii_lowercase() } else { letters[at].to_ascii_uppercase() };
    }
    letters.into_iter().collect()
}

fn main() {
    // 20,000 random words made once, then every word checked in each of
    // 200 rounds.
    let mut seed: i64 = 520;
    let words: Vec<String> = (0..20000).map(|_| random_word(&mut seed)).collect();
    let mut right: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..200i64 {
        for (i, w) in words.iter().enumerate() {
            if detect_capital_use(w) {
                right += 1;
                checksum = (checksum + (round + 1) * (i as i64 + 1)) % 1000000007;
            }
        }
    }
    println!("20000 words, 200 rounds: {} right, checksum {}", right, checksum);
}
