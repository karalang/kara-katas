// LeetCode #2405: Optimal Partition of String -- the bench, the ★ arm in
// Rust: greedy with a bitmask, a letter already in the current part
// starting the next one.

fn partition_string(s: &str) -> i64 {
    let (mut parts, mut seen) = (1i64, 0i64);
    for b in s.bytes() {
        let bit = 1i64 << (b - b'a');
        if seen & bit != 0 {
            parts += 1;
            seen = 0;
        }
        seen |= bit;
    }
    parts
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2405;
    let strings: Vec<String> = (0..26i64)
        .map(|i| (0..100000).map(|_| (b'a' + (next_random(&mut seed) % (i + 1)) as u8) as char).collect())
        .collect();
    let mut check: i64 = 0;
    for p in 0..50 {
        for s in &strings {
            check = (check * 31 + partition_string(s) + p) % 1000000007;
        }
    }
    println!("50 passes over 26 strings of 10^5 letters: checksum {}", check);
}
