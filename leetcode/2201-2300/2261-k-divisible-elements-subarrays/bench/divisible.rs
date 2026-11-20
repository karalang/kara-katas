// LeetCode #2261: K Divisible Elements Subarrays -- Rust mirror of the ★
// arm: from every start the subarray grows until more than k of its
// elements are divisible by p, each one put into a `HashSet<Vec<i64>>`.
// Same workload and checksum as divisible.kara.
use std::collections::HashSet;

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn count_distinct(nums: &[i64], k: i64, p: i64) -> i64 {
    let mut seen: HashSet<Vec<i64>> = HashSet::new();
    for start in 0..nums.len() {
        let mut divisible = 0;
        let mut run: Vec<i64> = Vec::new();
        for end in start..nums.len() {
            if nums[end] % p == 0 {
                divisible += 1;
            }
            if divisible > k {
                break;
            }
            run.push(nums[end]);
            seen.insert(run.clone());
        }
    }
    seen.len() as i64
}

fn main() {
    let mut seed = 2261;
    let mut check = 0;
    for _ in 0..40 {
        let nums: Vec<i64> = (0..200).map(|_| next_random(&mut seed) % 200 + 1).collect();
        let p = next_random(&mut seed) % 8 + 2;
        let k = next_random(&mut seed) % 196 + 5;
        check = (check * 31 + count_distinct(&nums, k, p)) % 1000000007;
    }
    println!("40 arrays of 200: checksum {}", check);
}
