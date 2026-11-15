// LeetCode #2154: Keep Multiplying Found Values by Two -- the benchmark's
// Rust mirror of doubling.kara.

use std::collections::HashSet;

fn find_final_value(nums: &[i64], original: i64) -> i64 {
    let found: HashSet<i64> = nums.iter().cloned().collect();
    let mut value = original;
    while found.contains(&value) {
        value *= 2;
    }
    value
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2154i64;
    let mut row: Vec<i64> = Vec::new();
    for _ in 0..400000 {
        row.push(next_random(&mut seed) % 1000 + 1);
    }
    let mut check = 0i64;
    for _ in 0..20000 {
        let a = next_random(&mut seed);
        let b = next_random(&mut seed);
        let start = ((a * 32768 + b) % 399001) as usize;
        let original = next_random(&mut seed) % 1000 + 1;
        let value = find_final_value(&row[start..start + 1000], original);
        check = (check * 31 + value) % 1000000007;
    }
    println!("20000 solves: checksum {}", check);
}
