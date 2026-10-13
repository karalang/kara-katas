// Benchmark for #521: Rust mirror of the ★ arm (the whole longer word);
// see find_lus_length.kara.

fn find_lus_length(a: &str, b: &str) -> i64 {
    if a == b { -1 } else { a.len().max(b.len()) as i64 }
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

fn main() {
    // 20,000 pairs of 1 to 100 letters from 1 to 3 letters made once (a
    // third equal, a third the first word with a letter added, a third
    // unrelated), then every pair answered in each of 5,000 rounds.
    let mut seed: i64 = 521;
    let mut firsts: Vec<String> = Vec::new();
    let mut seconds: Vec<String> = Vec::new();
    for i in 0..20000 {
        let letters = 1 + next_random(&mut seed) % 3;
        let len = 1 + next_random(&mut seed) % 100;
        let a = random_word(&mut seed, len, letters);
        let b = if i % 3 == 0 {
            a.clone()
        } else if i % 3 == 1 {
            let mut c = a.clone();
            c.push((97 + next_random(&mut seed) % letters) as u8 as char);
            c
        } else {
            let len = 1 + next_random(&mut seed) % 100;
            random_word(&mut seed, len, letters)
        };
        firsts.push(a);
        seconds.push(b);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..5000i64 {
        for i in 0..firsts.len() {
            let n = find_lus_length(&firsts[i], &seconds[i]);
            total += n;
            checksum = (checksum + (round + 1) * (n + 2)) % 1000000007;
        }
    }
    println!("20000 pairs, 5000 rounds: total {}, checksum {}", total, checksum);
}
