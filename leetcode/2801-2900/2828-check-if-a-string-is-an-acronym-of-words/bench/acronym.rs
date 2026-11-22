// LeetCode #2828: Check if a String Is an Acronym of Words -- the bench's
// Rust mirror of the ★ arm: the lengths first, then every word's first
// byte against s's byte at the same place.

fn is_acronym(words: &[String], s: &str) -> bool {
    words.len() == s.len() && words.iter().zip(s.bytes()).all(|(w, c)| w.as_bytes()[0] == c)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn word(seed: &mut i64) -> String {
    let n = next_random(seed) % 10 + 1;
    (0..n).map(|_| (97 + next_random(seed) % 3) as u8 as char).collect()
}

fn main() {
    let count = 20000;
    let rounds = 100;
    let mut seed = 2828;
    let mut cases: Vec<(Vec<String>, String)> = Vec::new();
    for _ in 0..count {
        let words: Vec<String> = (0..100).map(|_| word(&mut seed)).collect();
        let mut s: Vec<u8> = words.iter().map(|w| w.as_bytes()[0]).collect();
        if next_random(&mut seed) % 4 == 0 {
            let at = (next_random(&mut seed) % 100) as usize;
            s[at] = (97 + next_random(&mut seed) % 3) as u8;
        }
        cases.push((words, String::from_utf8(s).unwrap()));
    }
    let mut yes = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (words, s) in &cases {
            let a = is_acronym(words, s);
            if a {
                yes += 1;
            }
            check = (check * 31 + if a { 1 } else { 0 } + r) % 1000000007;
        }
    }
    println!("{} cases of 100 words, {} rounds: {} true, checksum {}", count, rounds, yes, check);
}
