// LeetCode #696: Count Binary Substrings -- bench program, Rust mirror of the ★ arm.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn count_binary_substrings(s: &str) -> i64 {
    let b = s.as_bytes();
    let mut before: i64 = 0;
    let mut current: i64 = 1;
    let mut count: i64 = 0;
    for i in 1..b.len() {
        if b[i] == b[i - 1] {
            current += 1;
        } else {
            count += before.min(current);
            before = current;
            current = 1;
        }
    }
    count + before.min(current)
}

fn main() {
    let mut seed = 696;
    let mut strings: Vec<String> = Vec::new();
    for k in 0..20 {
        let longest = 1 + 2 * k;
        let mut s = String::new();
        let mut bit = 0;
        while s.len() < 100000 {
            let run = 1 + next_random(&mut seed) % longest;
            for _ in 0..run {
                if s.len() < 100000 {
                    s.push(if bit == 0 { '0' } else { '1' });
                }
            }
            bit = 1 - bit;
        }
        strings.push(s);
    }
    let rounds = 150;
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        for s in &strings {
            let r = count_binary_substrings(s);
            total += r;
            checksum = (checksum * 31 + r) % 1000000007;
        }
    }
    println!("{} rounds of 20 strings of 100000: {} substrings counted, checksum {}", rounds, total, checksum);
}
