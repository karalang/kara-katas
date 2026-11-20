// LeetCode #1675: Minimize Deviation in Array -- the bench's Rust mirror:
// the ★ arm on 50 arrays of 50000 values up to 10^9, all drawn first, each
// answered 10 times, with `std::collections::BinaryHeap` (largest first).

use std::collections::BinaryHeap;

fn minimum_deviation(nums: &[i32]) -> i32 {
    let mut queue = BinaryHeap::with_capacity(nums.len());
    let mut smallest = i32::MAX;
    for &x in nums {
        let start = if x % 2 == 1 { x * 2 } else { x };
        queue.push(start);
        smallest = smallest.min(start);
    }
    let mut best = i32::MAX;
    loop {
        let top = queue.pop().unwrap();
        best = best.min(top - smallest);
        if top % 2 == 1 {
            break;
        }
        smallest = smallest.min(top / 2);
        queue.push(top / 2);
    }
    best
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let arrays = 50;
    let n = 50000;
    let rounds: i64 = 10;
    let mut seed: i64 = 1675;
    let mut cases: Vec<Vec<i32>> = Vec::new();
    for _ in 0..arrays {
        let mut nums: Vec<i32> = Vec::new();
        for _ in 0..n {
            nums.push(((next_random(&mut seed) * 32768 + next_random(&mut seed)) % 1000000000 + 1) as i32);
        }
        cases.push(nums);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for nums in &cases {
            let deviation = minimum_deviation(nums) as i64;
            total += deviation;
            check = (check * 31 + deviation + r) % 1000000007;
        }
    }
    println!("{} arrays of {} values, {} rounds: deviations sum to {}, checksum {}", arrays, n, rounds, total, check);
}
