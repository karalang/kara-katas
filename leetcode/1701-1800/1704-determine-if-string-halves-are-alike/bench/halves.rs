// LeetCode #1704: Determine if String Halves Are Alike -- the bench's
// Rust mirror: the ★ arm on 1000 random strings of 1000 letters, all
// drawn first, each answered 400 times.

// one pass: a vowel in the first half counted up and in the second down
fn halves_are_alike(s: &str) -> bool {
    let bytes = s.as_bytes();
    let half = bytes.len() / 2;
    let mut balance: i64 = 0;
    for (i, &b) in bytes.iter().enumerate() {
        match b {
            b'a' | b'e' | b'i' | b'o' | b'u' | b'A' | b'E' | b'I' | b'O' | b'U' => {
                balance += if i < half { 1 } else { -1 };
            }
            _ => {}
        }
    }
    balance == 0
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 1000;
    let rounds = 400;
    let n = 1000;
    let mut seed = 1704;
    let vowels = "aeiouAEIOU".as_bytes();
    let consonants = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ".as_bytes();
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..count {
        // each letter a vowel with a chance of its string's own, 0 to 10 in 10
        let lean = next_random(&mut seed) % 11;
        let mut s = String::with_capacity(n);
        for _ in 0..n {
            let b = if next_random(&mut seed) % 10 < lean {
                vowels[(next_random(&mut seed) % vowels.len() as i64) as usize]
            } else {
                consonants[(next_random(&mut seed) % consonants.len() as i64) as usize]
            };
            s.push(b as char);
        }
        strings.push(s);
    }
    let mut alike: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for s in strings.iter() {
            let answer = halves_are_alike(s);
            if answer {
                alike += 1;
            }
            check = (check * 31 + if answer { 1 } else { 2 } + r) % 1000000007;
        }
    }
    println!("{count} strings of {n} letters, {rounds} rounds: {alike} alike, checksum {check}");
}
