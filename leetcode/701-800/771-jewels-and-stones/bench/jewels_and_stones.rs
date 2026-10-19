// LeetCode 771 — Jewels and Stones: benchmark, the ★ arm in Rust.
// 256 random pairs of 50 jewels and 50 stones, built once; ROUNDS rounds
// each count the next pair. HashSet<char> hashes with SipHash-1-3.
use std::collections::HashSet;

const ROUNDS: i64 = 1000000;

fn num_jewels_in_stones(jewels: &str, stones: &str) -> i64 {
    let mut kinds: HashSet<char> = HashSet::new();
    for c in jewels.chars() {
        kinds.insert(c);
    }
    let mut count = 0;
    for c in stones.chars() {
        if kinds.contains(&c) {
            count += 1;
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_letters(seed: &mut i64, n: i64, kinds: i64) -> String {
    let mut out = String::new();
    for _ in 0..n {
        let k = next_random(seed) % kinds;
        let base = if k % 2 == 0 { 97 } else { 65 };
        out.push((base + k / 2) as u8 as char);
    }
    out
}

fn main() {
    let mut seed = 771;
    let mut jewels: Vec<String> = Vec::new();
    let mut stones: Vec<String> = Vec::new();
    for _ in 0..256 {
        jewels.push(random_letters(&mut seed, 50, 52));
        stones.push(random_letters(&mut seed, 50, 52));
    }
    let mut total = 0;
    let mut check: i64 = 0;
    for round in 0..ROUNDS {
        let k = (round % 256) as usize;
        let count = num_jewels_in_stones(&jewels[k], &stones[k]);
        total += count;
        check = (check * 31 + count) % 1000000007;
    }
    println!("{ROUNDS} rounds of 50 jewels and 50 stones: {total} jewels in all, checksum {check}");
}
