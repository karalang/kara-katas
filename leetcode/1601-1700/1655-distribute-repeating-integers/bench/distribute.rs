// LeetCode #1655: Distribute Repeating Integers -- the bench's Rust
// mirror: the ★ arm on 200 random problems of 100000 numbers from 50
// values and 10 customers wanting 1 to 3000 each, all drawn first.

use std::collections::HashMap;

fn can_distribute(nums: &[i32], quantity: &[i32]) -> bool {
    let mut counts: HashMap<i32, i64> = HashMap::new();
    for &x in nums {
        *counts.entry(x).or_insert(0) += 1;
    }
    let m = quantity.len();
    let full: usize = (1 << m) - 1;
    let mut want = vec![0i64; 1 << m];
    for mask in 1..=full {
        let low = mask.trailing_zeros() as usize;
        want[mask] = want[mask & (mask - 1)] + quantity[low] as i64;
    }
    let mut can = vec![false; 1 << m];
    can[0] = true;
    for &count in counts.values() {
        let before = can.clone();
        for mask in 0..=full {
            if !before[mask] {
                continue;
            }
            let rest = full & !mask;
            let mut sub = rest;
            while sub > 0 {
                if want[sub] <= count {
                    can[mask | sub] = true;
                }
                sub = (sub - 1) & rest;
            }
        }
    }
    can[full]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1655;
    let mut problems: Vec<(Vec<i32>, Vec<i32>)> = Vec::new();
    for _ in 0..200 {
        let nums: Vec<i32> = (0..100000).map(|_| (next_random(&mut seed) % 50 + 1) as i32).collect();
        let quantity: Vec<i32> = (0..10).map(|_| (next_random(&mut seed) % 3000 + 1) as i32).collect();
        problems.push((nums, quantity));
    }
    let mut check: i64 = 0;
    let mut served = 0;
    for (nums, quantity) in &problems {
        let answer = can_distribute(nums, quantity);
        if answer {
            served += 1;
        }
        check = (check * 31 + if answer { 2 } else { 1 }) % 1000000007;
    }
    println!("200 problems of 100000 numbers and 10 customers: {} served, checksum {}", served, check);
}
