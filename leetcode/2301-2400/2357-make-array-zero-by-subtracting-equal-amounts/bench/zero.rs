// LeetCode #2357: Make Array Zero by Subtracting Equal Amounts -- the
// bench, the ★ arm in Rust: the distinct positive values gathered in a
// `HashSet`.

use std::collections::HashSet;

fn minimum_operations(nums: &[i64]) -> i64 {
    let mut seen: HashSet<i64> = HashSet::new();
    for &x in nums {
        if x > 0 {
            seen.insert(x);
        }
    }
    seen.len() as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 2 * 10^4 arrays of 100 values from 0 to 1 up to 0 to 100
    let mut seed = 2357i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20000 {
        let top = 2 + next_random(&mut seed) % 100;
        let nums: Vec<i64> = (0..100).map(|_| next_random(&mut seed) % top).collect();
        arrays.push(nums);
    }
    let mut check = 0i64;
    for p in 0..50i64 {
        for nums in &arrays {
            check = (check * 31 + minimum_operations(nums) + p) % 1000000007;
        }
    }
    println!("50 passes over 2 * 10^4 arrays of 100 values: checksum {}", check);
}
