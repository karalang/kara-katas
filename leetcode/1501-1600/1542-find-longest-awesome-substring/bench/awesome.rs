// LeetCode #1542: Find Longest Awesome Substring -- bench: the ★ arm (prefix
// parity masks, first places in a Vec) over 100 strings of 1 to 100000
// digits, each over its own first 1 to 10, built once, each asked 4 times.
// Rust mirror of awesome.kara.

fn longest_awesome(s: &str) -> i64 {
    let n = s.len() as i64;
    let mut first = vec![n + 1; 1024];
    first[0] = 0;
    let mut mask = 0usize;
    let mut best = 0i64;
    for (i, c) in s.bytes().enumerate() {
        mask ^= 1 << (c - b'0');
        let end = i as i64 + 1;
        best = best.max(end - first[mask]);
        for d in 0..10 {
            best = best.max(end - first[mask ^ (1 << d)]);
        }
        if first[mask] > n {
            first[mask] = end;
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1542i64;
    let mut strings = Vec::new();
    for _ in 0..100 {
        let n = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 100000 + 1;
        let digits = next_random(&mut seed) % 10 + 1;
        let mut s = String::new();
        for _ in 0..n {
            s.push((b'0' + (next_random(&mut seed) % digits) as u8) as char);
        }
        strings.push(s);
    }
    let mut check = 0i64;
    for _ in 0..4 {
        for s in &strings {
            check = mix(check, longest_awesome(s));
        }
    }
    println!("4 passes over 100 strings of up to 100000 digits: checksum {}", check);
}
