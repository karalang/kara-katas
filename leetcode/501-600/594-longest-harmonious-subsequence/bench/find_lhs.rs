// Benchmark for #594: Rust mirror of the ★ arm (count in a map, then
// pair); see find_lhs.kara. `HashMap` with its default hasher,
// SipHash-1-3 under a random key, as Kāra's `Map` hashes.

use std::collections::HashMap;

fn find_lhs(nums: &[i64]) -> i64 {
    let mut count: HashMap<i64, i64> = HashMap::new();
    for &x in nums {
        *count.entry(x).or_insert(0) += 1;
    }
    let mut best = 0;
    for (&v, &c) in &count {
        if let Some(&d) = count.get(&(v + 1)) {
            best = best.max(c + d);
        }
    }
    best
}

// ---- benchmark --------------------------------------------------------------

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let hi = step(seed);
    let lo = step(seed);
    hi * 32768 + lo
}

fn main() {
    let count = 100;
    let rounds = 20;
    let mut seed: i64 = 594;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let range = 1 + wide(&mut seed) % 5000;
        let low = wide(&mut seed) % 1999990000 - 999990000;
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..20000 {
            nums.push(low + wide(&mut seed) % range);
        }
        arrays.push(nums);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for g in 0..count {
            let got = find_lhs(&arrays[(round * 7 + g) % count]);
            total += got;
            checksum = (checksum * 31 + got) % 1000000007;
        }
    }
    println!("{} arrays, {} rounds: total {}, checksum {}", count, rounds, total, checksum);
}
