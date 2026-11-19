// LeetCode #1636: Sort Array by Increasing Frequency -- the bench's Rust
// mirror: the ★ arm on 50000 random arrays of 100 values from -100 to 100,
// all drawn first.

use std::collections::HashMap;

fn frequency_sort(nums: &Vec<i32>) -> Vec<i32> {
    let mut count: HashMap<i32, i64> = HashMap::new();
    for &x in nums {
        *count.entry(x).or_insert(0) += 1;
    }
    let mut sorted = nums.clone();
    sorted.sort_by_key(|x| (count[x], -x));
    sorted
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1636;
    let mut arrays: Vec<Vec<i32>> = Vec::new();
    for _ in 0..50000 {
        let mut nums = Vec::new();
        for _ in 0..100 {
            nums.push((next_random(&mut seed) % 201 - 100) as i32);
        }
        arrays.push(nums);
    }
    let mut check: i64 = 0;
    for nums in &arrays {
        for x in frequency_sort(nums) {
            check = (check * 31 + x as i64 + 1000) % 1000000007;
        }
    }
    println!("50000 arrays of 100 values: checksum {}", check);
}
