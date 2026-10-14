// Benchmark for #557: Rust mirror of the ★ arm (split, reverse, join);
// see reverse_words_in_a_string_iii.kara.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn reverse_words(s: &str) -> String {
    let mut words: Vec<String> = Vec::new();
    for w in s.split(' ') {
        let r: String = w.chars().rev().collect();
        words.push(r);
    }
    words.join(" ")
}

fn main() {
    let count = 100;
    let mut seed: i64 = 557;
    let mut texts: Vec<String> = Vec::new();
    let mut words = 0;
    for _ in 0..count {
        let mut s = String::new();
        while s.len() < 49980 {
            if !s.is_empty() {
                s.push(' ');
            }
            let length = 1 + next_random(&mut seed) % 12;
            for _ in 0..length {
                s.push((b'!' + (next_random(&mut seed) % 94) as u8) as char);
            }
            words += 1;
        }
        texts.push(s);
    }
    let mut checksum: i64 = 0;
    for round in 0..50 {
        for g in 0..count {
            let got = reverse_words(&texts[(round * 7 + g) % count]);
            let b = got.as_bytes();
            checksum = (checksum * 31 + b.len() as i64 + b[0] as i64 * 7 + b[b.len() / 2] as i64) % 1000000007;
        }
    }
    println!("{} texts, {} words, 50 rounds each: checksum {}", count, words, checksum);
}
