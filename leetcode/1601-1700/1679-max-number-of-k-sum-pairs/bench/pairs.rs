// LeetCode #1679: Max Number of K-Sum Pairs -- the bench's Rust mirror: the
// ★ arm on 50 arrays of 100000 values up to 100000, each with a k up to
// 200000, all drawn first, each answered 10 times, with a `HashMap`.

use std::collections::HashMap;

fn max_operations(nums: &[i32], k: i32) -> i32 {
    let mut waiting: HashMap<i32, i32> = HashMap::new();
    let mut operations = 0;
    for &x in nums {
        let partner = k - x;
        match waiting.get_mut(&partner) {
            Some(c) if *c > 0 => {
                *c -= 1;
                operations += 1;
            }
            _ => {
                *waiting.entry(x).or_insert(0) += 1;
            }
        }
    }
    operations
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let arrays = 50;
    let n = 100000;
    let most: i64 = 100000;
    let rounds: i64 = 10;
    let mut seed: i64 = 1679;
    let mut cases: Vec<(Vec<i32>, i32)> = Vec::new();
    for _ in 0..arrays {
        let mut nums: Vec<i32> = Vec::new();
        for _ in 0..n {
            nums.push(((next_random(&mut seed) * 32768 + next_random(&mut seed)) % most + 1) as i32);
        }
        let k = ((next_random(&mut seed) * 32768 + next_random(&mut seed)) % (2 * most - 1) + 2) as i32;
        cases.push((nums, k));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (nums, k) in &cases {
            let operations = max_operations(nums, *k) as i64;
            total += operations;
            check = (check * 31 + operations + r) % 1000000007;
        }
    }
    println!("{} arrays of {} values, {} rounds: {} operations, checksum {}", arrays, n, rounds, total, check);
}
