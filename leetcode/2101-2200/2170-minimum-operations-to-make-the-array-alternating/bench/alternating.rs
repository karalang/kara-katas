// LeetCode #2170: Minimum Operations to Make the Array Alternating -- the
// benchmark's Rust mirror of alternating.kara.

use std::collections::HashMap;

fn top_two(nums: &[i64], start: usize) -> ((i64, i64), (i64, i64)) {
    let mut counts: HashMap<i64, i64> = HashMap::new();
    let mut i = start;
    while i < nums.len() {
        *counts.entry(nums[i]).or_insert(0) += 1;
        i += 2;
    }
    let mut first = (0i64, 0i64);
    let mut second = (0i64, 0i64);
    for (&value, &count) in counts.iter() {
        if count > first.1 {
            second = first;
            first = (value, count);
        } else if count > second.1 {
            second = (value, count);
        }
    }
    (first, second)
}

fn minimum_operations(nums: &[i64]) -> i64 {
    let n = nums.len() as i64;
    let (even_first, even_second) = top_two(nums, 0);
    let (odd_first, odd_second) = top_two(nums, 1);
    if even_first.0 != odd_first.0 {
        n - even_first.1 - odd_first.1
    } else {
        n - (even_first.1 + odd_second.1).max(even_second.1 + odd_first.1)
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2170i64;
    let mut row: Vec<i64> = Vec::new();
    for _ in 0..400000 {
        let a = next_random(&mut seed);
        let b = next_random(&mut seed);
        row.push((a * 32768 + b) % 1000 + 1);
    }
    let mut check = 0i64;
    for _ in 0..100 {
        let a = next_random(&mut seed);
        let b = next_random(&mut seed);
        let start = ((a * 32768 + b) % 300001) as usize;
        let ops = minimum_operations(&row[start..start + 100000]);
        check = (check * 31 + ops) % 1000000007;
    }
    println!("100 solves: checksum {}", check);
}
