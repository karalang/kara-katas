// Benchmark for #491: Rust mirror of the ★ arm (backtracking); see
// non_decreasing_subsequences.kara.
use std::collections::HashSet;

fn extend(nums: &[i64], from: usize, current: &mut Vec<i64>, out: &mut Vec<Vec<i64>>) {
    if current.len() >= 2 {
        out.push(current.clone());
    }
    let mut tried: HashSet<i64> = HashSet::new();
    for i in from..nums.len() {
        if tried.contains(&nums[i]) {
            continue;
        }
        if current.is_empty() || nums[i] >= current[current.len() - 1] {
            tried.insert(nums[i]);
            current.push(nums[i]);
            extend(nums, i + 1, current, out);
            current.pop();
        }
    }
}

fn find_subsequences(nums: &[i64]) -> Vec<Vec<i64>> {
    let mut out: Vec<Vec<i64>> = Vec::new();
    let mut current: Vec<i64> = Vec::new();
    extend(nums, 0, &mut current, &mut out);
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 3000 arrays of 15 numbers, the k-th from k / 2 to k / 2 + 3, so
    // they mostly rise, built once, then each solved once.
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    let mut seed: i64 = 491;
    for _ in 0..3000 {
        let mut nums: Vec<i64> = Vec::new();
        for k in 0..15 {
            nums.push(k / 2 + next_random(&mut seed) % 4);
        }
        arrays.push(nums);
    }
    let mut total = 0;
    let mut checksum: i64 = 0;
    for nums in &arrays {
        let out = find_subsequences(nums);
        total += out.len();
        for s in &out {
            for x in s {
                checksum = (checksum * 31 + x + 7) % 1000000007;
            }
            checksum = (checksum * 31 + 15) % 1000000007;
        }
    }
    println!("3000 arrays of 15: {total} subsequences, checksum {checksum}");
}
