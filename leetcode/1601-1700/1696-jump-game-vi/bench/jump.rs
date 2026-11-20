// LeetCode #1696: Jump Game VI -- the bench's Rust mirror: the ★ arm on 50
// random arrays of 100000 values from -10^4 to 10^4, each with a random k
// up to 100000, all drawn first, each answered 20 times.

use std::collections::VecDeque;

fn max_result(nums: &[i32], k: i32) -> i32 {
    let k = k as i64;
    let mut best = vec![0i32; nums.len()];
    best[0] = nums[0];
    let mut reach: VecDeque<i64> = VecDeque::new();
    reach.push_back(0);
    for i in 1..nums.len() as i64 {
        if reach[0] < i - k {
            reach.pop_front();
        }
        best[i as usize] = nums[i as usize] + best[reach[0] as usize];
        while !reach.is_empty() && best[reach[reach.len() - 1] as usize] <= best[i as usize] {
            reach.pop_back();
        }
        reach.push_back(i);
    }
    best[nums.len() - 1]
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 50;
    let rounds = 20;
    let n: i64 = 100000;
    let mut seed = 1696;
    let mut arrays: Vec<Vec<i32>> = Vec::new();
    let mut ks: Vec<i32> = Vec::new();
    for _ in 0..count {
        let mut nums: Vec<i32> = Vec::new();
        for _ in 0..n {
            nums.push((next_random(&mut seed) % 20001 - 10000) as i32);
        }
        arrays.push(nums);
        let hi = next_random(&mut seed);
        ks.push(((hi * 32768 + next_random(&mut seed)) % n + 1) as i32);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (c, nums) in arrays.iter().enumerate() {
            let answer = max_result(nums, ks[c]) as i64;
            total += answer;
            check = ((check * 31 + answer + r) % 1000000007 + 1000000007) % 1000000007;
        }
    }
    println!("{count} arrays of {n} values, {rounds} rounds: answers sum to {total}, checksum {check}");
}
