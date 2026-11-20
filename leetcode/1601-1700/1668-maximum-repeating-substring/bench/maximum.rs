// LeetCode #1668: Maximum Repeating Substring -- the bench's Rust mirror:
// the ★ arm on 400000 problems, words of 1 to 6 letters and sequences of
// about 100 built of whole copies of the word and single letters, all
// drawn first.

fn max_repeating(sequence: &str, word: &str) -> i32 {
    let mut k = 0;
    let mut repeated = word.to_string();
    while sequence.contains(repeated.as_str()) {
        k += 1;
        repeated.push_str(word);
    }
    k
}

// ---- the harness --------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_text(n: i64, kinds: i64, seed: &mut i64) -> String {
    let mut text = String::new();
    for _ in 0..n {
        text.push((b'a' + (next_random(seed) % kinds) as u8) as char);
    }
    text
}

fn random_sequence(word: &str, n: usize, kinds: i64, seed: &mut i64) -> String {
    let mut text = String::new();
    while text.len() < n {
        if next_random(seed) % 2 == 0 {
            text.push_str(word);
        } else {
            text.push_str(&random_text(1, kinds, seed));
        }
    }
    text
}

fn main() {
    let problems = 400000;
    let mut seed: i64 = 1668;
    let mut cases: Vec<(String, String)> = Vec::new();
    for _ in 0..problems {
        let kinds = next_random(&mut seed) % 3 + 1;
        let len = next_random(&mut seed) % 6 + 1;
        let word = random_text(len, kinds, &mut seed);
        let sequence = random_sequence(&word, 100, kinds, &mut seed);
        cases.push((sequence, word));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for (sequence, word) in &cases {
        let k = max_repeating(sequence, word) as i64;
        total += k;
        check = (check * 31 + k) % 1000000007;
    }
    println!("{} problems of about 100 letters: answers sum to {}, checksum {}", problems, total, check);
}
