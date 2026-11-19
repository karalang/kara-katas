// LeetCode #1653: Minimum Deletions to Make String Balanced -- the bench's
// Rust mirror: the ★ arm on 500 random strings of 100000 a's and b's,
// each with its own chance of a b, all drawn first.

fn minimum_deletions(s: &str) -> i64 {
    let mut deletions: i64 = 0;
    let mut bs: i64 = 0;
    for c in s.chars() {
        if c == 'b' {
            bs += 1;
        } else {
            deletions = (deletions + 1).min(bs);
        }
    }
    deletions
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1653;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..500 {
        let percent = next_random(&mut seed) % 101;
        let mut s = String::new();
        for _ in 0..100000 {
            s.push(if next_random(&mut seed) % 100 < percent { 'b' } else { 'a' });
        }
        strings.push(s);
    }
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for s in &strings {
        let deletions = minimum_deletions(s);
        total += deletions;
        check = (check * 31 + deletions + 1) % 1000000007;
    }
    println!("500 strings of 100000 letters: deletions sum to {}, checksum {}", total, check);
}
