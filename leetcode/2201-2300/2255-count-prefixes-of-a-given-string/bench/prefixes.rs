// LeetCode #2255: Count Prefixes of a Given String -- the benchmark's Rust
// mirror of prefixes.kara: each word tested with `s.starts_with(word)` and
// the ones that hold counted by `filter` and `count`.

fn count_prefixes(words: &[String], s: &str) -> i64 {
    words.iter().filter(|w| s.starts_with(w.as_str())).count() as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(seed: &mut i64, longest: i64, letters: i64) -> String {
    let length = next_random(seed) % longest + 1;
    (0..length).map(|_| (b'a' + (next_random(seed) % letters) as u8) as char).collect()
}

fn main() {
    let mut seed = 2255i64;
    let mut check = 0i64;
    for c in 0..500 {
        let letters = c % 5 + 1;
        let words: Vec<String> = (0..1000).map(|_| random_word(&mut seed, 10, letters)).collect();
        let s = random_word(&mut seed, 10, letters);
        check = (check * 31 + count_prefixes(&words, &s) + 1) % 1000000007;
    }
    println!("500 cases of 1000 words: checksum {}", check);
}
