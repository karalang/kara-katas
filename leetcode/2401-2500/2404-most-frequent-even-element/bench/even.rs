// LeetCode #2404: Most Frequent Even Element -- the bench, the ★ arm in
// Rust: a `HashMap` of counts of the even values, then every entry read
// for the most frequent and the smallest among equal counts.

use std::collections::HashMap;

fn most_frequent_even(nums: &[i64]) -> i64 {
    let mut count: HashMap<i64, i64> = HashMap::new();
    for &x in nums {
        if x % 2 == 0 {
            *count.entry(x).or_insert(0) += 1;
        }
    }
    let (mut best, mut most) = (-1i64, 0i64);
    for (&x, &c) in &count {
        if c > most || c == most && x < best {
            best = x;
            most = c;
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2404;
    let arrays: Vec<Vec<i64>> = (0..200i64).map(|i| (0..2000).map(|_| next_random(&mut seed) % (1 + 50 * i)).collect()).collect();
    let mut check: i64 = 0;
    for p in 0..100 {
        for nums in &arrays {
            check = (check * 31 + most_frequent_even(nums) + 1 + p) % 1000000007;
        }
    }
    println!("100 passes over 200 arrays of 2000 values: checksum {}", check);
}
