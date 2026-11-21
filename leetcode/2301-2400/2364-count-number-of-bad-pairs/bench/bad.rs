// LeetCode #2364: Count Number of Bad Pairs -- the bench, the ★ arm in
// Rust: each place's key nums[j] - j counted in a `HashMap` as the places
// go by, the places before j with the same key its good pairs, and the
// bad pairs all n (n - 1) / 2 less the good ones.

use std::collections::HashMap;

fn count_bad_pairs(nums: &[i64]) -> i64 {
    let n = nums.len() as i64;
    let mut seen: HashMap<i64, i64> = HashMap::new();
    let mut good = 0i64;
    for (j, &x) in nums.iter().enumerate() {
        let key = x - j as i64;
        let before = *seen.get(&key).unwrap_or(&0);
        good += before;
        seen.insert(key, before + 1);
    }
    n * (n - 1) / 2 - good
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    hi * 32768 + next_random(seed)
}

fn main() {
    // array a: 10^5 values, each the place plus one of 4^a offsets (at
    // most 10^5) below 999 * 10^6, so the keys run from one to tens of
    // thousands
    let mut seed = 2364i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for a in 0..10 {
        let kinds = 1usize << (2 * a);
        let offsets: Vec<i64> = (0..kinds.min(100000)).map(|_| wide_random(&mut seed) % 999000000).collect();
        let nums: Vec<i64> = (0..100000i64).map(|i| 1 + i + offsets[(wide_random(&mut seed) % offsets.len() as i64) as usize]).collect();
        arrays.push(nums);
    }
    let mut check = 0i64;
    for p in 0..20i64 {
        for nums in &arrays {
            check = (check * 31 + count_bad_pairs(nums) % 1000000007 + p) % 1000000007;
        }
    }
    println!("20 passes over 10 arrays of 10^5 values: checksum {}", check);
}
