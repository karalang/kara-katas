// LeetCode #2395: Find Subarrays With Equal Sum -- the bench, the ★ arm in
// Rust: each neighbouring pair's sum into a HashSet, a sum already there
// the answer.

use std::collections::HashSet;

fn find_subarrays(nums: &[i64]) -> bool {
    let mut seen: HashSet<i64> = HashSet::new();
    for i in 1..nums.len() {
        let sum = nums[i - 1] + nums[i];
        if seen.contains(&sum) {
            return true;
        }
        seen.insert(sum);
    }
    false
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2395i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..100 {
        let top = 1000 + wide(&mut seed) % 1000000;
        arrays.push((0..1000).map(|_| wide(&mut seed) % (2 * top + 1) - top).collect());
    }
    let mut check = 0i64;
    let mut yes = 0;
    for p in 0..2000i64 {
        for a in &arrays {
            let found = find_subarrays(a);
            check = (check * 31 + if found { 2 } else { 1 } + p) % 1000000007;
            if found {
                yes += 1;
            }
        }
    }
    println!("2000 passes over 100 arrays of 1000 values: checksum {}, {} yes", check, yes);
}
