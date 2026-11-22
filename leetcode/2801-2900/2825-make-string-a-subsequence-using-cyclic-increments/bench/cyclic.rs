// LeetCode #2825: Make String a Subsequence Using Cyclic Increments --
// the bench's Rust mirror of the ★ arm: two pointers over the bytes.

fn can_make_subsequence(str1: &str, str2: &str) -> bool {
    let (a, b) = (str1.as_bytes(), str2.as_bytes());
    let mut j = 0;
    for &c in a {
        if j == b.len() {
            break;
        }
        let next = if c == b'z' { b'a' } else { c + 1 };
        if c == b[j] || next == b[j] {
            j += 1;
        }
    }
    j == b.len()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn letters(n: i64, from: i64, width: i64, seed: &mut i64) -> String {
    (0..n).map(|_| (((from + next_random(seed) % width) % 26 + 97) as u8) as char).collect()
}

fn main() {
    let count = 100;
    let rounds = 50;
    let mut seed = 2825;
    let mut pairs: Vec<(String, String)> = Vec::new();
    for _ in 0..count {
        let s1 = letters(100000, 23, 6, &mut seed);
        let m = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 50000 + 1;
        pairs.push((s1, letters(m, 23, 6, &mut seed)));
    }
    let mut yes = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (s1, s2) in &pairs {
            let a = can_make_subsequence(s1, s2);
            if a {
                yes += 1;
            }
            check = (check * 31 + if a { 1 } else { 0 } + r) % 1000000007;
        }
    }
    println!("{} pairs of 100000, {} rounds: {} true, checksum {}", count, rounds, yes, check);
}
