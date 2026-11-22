// LeetCode #2762: Continuous Subarrays -- the bench (continuous.kara in
// Rust): a window with two `VecDeque`s of indices whose fronts are its
// least and greatest, shrunk from the left while those lie more than 2
// apart.
use std::collections::VecDeque;

fn continuous_subarrays(nums: &[i64]) -> i64 {
    let mut lows: VecDeque<usize> = VecDeque::new();
    let mut highs: VecDeque<usize> = VecDeque::new();
    let mut left = 0;
    let mut count: i64 = 0;
    for right in 0..nums.len() {
        let v = nums[right];
        while let Some(&back) = lows.back() {
            if nums[back] <= v {
                break;
            }
            lows.pop_back();
        }
        while let Some(&back) = highs.back() {
            if nums[back] >= v {
                break;
            }
            highs.pop_back();
        }
        lows.push_back(right);
        highs.push_back(right);
        while nums[highs[0]] - nums[lows[0]] > 2 {
            left += 1;
            if lows[0] < left {
                lows.pop_front();
            }
            if highs[0] < left {
                highs.pop_front();
            }
        }
        count += (right - left + 1) as i64;
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 20;
    let rounds = 10;
    let mut seed = 2762;
    let mut cases: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut value: i64 = 500000000;
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..100000 {
            value += next_random(&mut seed) % 5 - 2;
            nums.push(value);
        }
        cases.push(nums);
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for nums in cases.iter() {
            let found = continuous_subarrays(nums);
            sum += found;
            check = (check * 31 + found + r) % 1000000007;
        }
    }
    println!("{count} walks of 100000, {rounds} rounds: subarrays sum to {sum}, checksum {check}");
}
