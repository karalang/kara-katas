// LeetCode #1218: Longest Arithmetic Subsequence of Given Difference --
// the bench in Rust: the ★ arm (a `HashMap` from each value to the
// longest subsequence ending with it) on the same 16 arrays of 10^5
// values and differences -3 to 3.
use std::collections::HashMap;

fn longest_subsequence(arr: &[i64], difference: i64) -> i64 {
    let mut ending: HashMap<i64, i64> = HashMap::new();
    let mut best = 0;
    for &x in arr.iter() {
        let length = ending.get(&(x - difference)).copied().unwrap_or(0) + 1;
        ending.insert(x, length);
        best = best.max(length);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1218;
    let mut arrays = Vec::new();
    for _ in 0..16 {
        let arr: Vec<i64> = (0..100000).map(|_| next_random(&mut seed) % 20001 - 10000).collect();
        arrays.push(arr);
    }
    let mut check: i64 = 0;
    for arr in arrays.iter() {
        for d in -3..=3i64 {
            check = (check * 131 + longest_subsequence(arr, d) + d + 3) % 1000000007;
        }
    }
    println!("16 arrays of 10^5 values, differences -3 to 3: checksum {}", check);
}
