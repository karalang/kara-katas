// LeetCode #1546: Maximum Number of Non-Overlapping Subarrays With Sum Equals
// Target -- bench: the ★ arm (greedy, a set of prefix sums cleared at each
// cut) over 100 arrays of 1 to 100000 values in -10..10, each with a target
// in -20..20, built once, each asked 5 times. Rust mirror of subarrays.kara,
// with std's HashSet.

use std::collections::HashSet;

fn max_non_overlapping(nums: &[i64], target: i64) -> i64 {
    let mut seen: HashSet<i64> = HashSet::new();
    seen.insert(0);
    let mut sum = 0i64;
    let mut count = 0i64;
    for &x in nums {
        sum += x;
        if seen.contains(&(sum - target)) {
            count += 1;
            seen.clear();
            seen.insert(0);
            sum = 0;
        } else {
            seen.insert(sum);
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1546i64;
    let mut cases = Vec::new();
    for _ in 0..100 {
        let n = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 100000 + 1;
        let mut nums = Vec::new();
        for _ in 0..n {
            nums.push(next_random(&mut seed) % 21 - 10);
        }
        let target = next_random(&mut seed) % 41 - 20;
        cases.push((nums, target));
    }
    let mut check = 0i64;
    let mut total = 0i64;
    for _ in 0..5 {
        for (nums, target) in &cases {
            let answer = max_non_overlapping(nums, *target);
            total += answer;
            check = mix(check, answer);
        }
    }
    println!("5 passes over 100 arrays of up to 100000 values: {} subarrays, checksum {}", total, check);
}
