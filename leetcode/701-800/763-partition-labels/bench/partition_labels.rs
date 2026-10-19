// LeetCode 763 — Partition Labels: benchmark, the ★ arm in Rust.
// 100,000 random strings of 500 letters.

fn partition_labels(s: &str) -> Vec<i64> {
    let bytes = s.as_bytes();
    let mut last = [0i64; 26];
    for (i, &c) in bytes.iter().enumerate() {
        last[(c - b'a') as usize] = i as i64;
    }
    let mut sizes = Vec::new();
    let (mut start, mut end) = (0i64, 0i64);
    for (i, &c) in bytes.iter().enumerate() {
        end = end.max(last[(c - b'a') as usize]);
        if i as i64 == end {
            sizes.push(end - start + 1);
            start = i as i64 + 1;
        }
    }
    sizes
}

fn main() {
    let mut seed: i64 = 763;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let rounds = 100000;
    let letters = "abcdefghijklmnopqrstuvwxyz";
    let mut parts: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        let width = 1 + next_random() % 4;
        let mut s = String::new();
        for i in 0..500i64 {
            let k = (i * 26 / 500 + next_random() % width).min(25) as usize;
            s.push_str(&letters[k..k + 1]);
        }
        let sizes = partition_labels(&s);
        parts += sizes.len() as i64;
        for size in &sizes {
            check = (check * 31 + size) % 1000000007;
        }
    }
    println!("{} strings of 500 letters: {} parts, checksum {}", rounds, parts, check);
}
