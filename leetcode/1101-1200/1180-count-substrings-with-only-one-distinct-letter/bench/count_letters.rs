// LeetCode #1180: Count Substrings with Only One Distinct Letter -- the ★
// arm's bench in Rust: one pass, the run of equal letters ending at each
// position added at every step. The same strings and the same 100 rounds.

fn count_letters(s: &str) -> i64 {
    let mut total: i64 = 0;
    let mut run: i64 = 0;
    let mut last = 0u8;
    for c in s.bytes() {
        if c == last {
            run += 1;
        } else {
            run = 1;
            last = c;
        }
        total += run;
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1180;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..1000 {
        let m = 1 + next_random(&mut seed) % 4;
        let bytes: Vec<u8> = (0..1000).map(|_| b'a' + (next_random(&mut seed) % m) as u8).collect();
        strings.push(String::from_utf8(bytes).unwrap());
    }
    let rounds = 100;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        for s in strings.iter() {
            check = (check * 131 + count_letters(s)) % 1000000007;
        }
    }
    println!("{} rounds of 1000 strings: checksum {}", rounds, check);
}
