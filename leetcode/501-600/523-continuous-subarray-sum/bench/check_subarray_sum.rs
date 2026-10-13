// Benchmark for #523: Rust mirror of the ★ arm (first index of each
// prefix remainder); see check_subarray_sum.kara. `HashMap` with its
// default hasher, as the ★ arm's `Map`.
use std::collections::HashMap;

fn check_subarray_sum(nums: &[i64], k: i64) -> bool {
    let mut first: HashMap<i64, i64> = HashMap::new();
    first.insert(0, -1);
    let mut rem = 0;
    for i in 0..nums.len() as i64 {
        rem = (rem + nums[i as usize]) % k;
        match first.get(&rem) {
            Some(&j) => {
                if i - j >= 2 {
                    return true;
                }
            }
            None => {
                first.insert(rem, i);
            }
        }
    }
    false
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 20 random arrays of 100,000 numbers from 1 to 20,000 (the
    // problem's longest, summing under 2^31) made once; then each checked
    // in 10 rounds against a fresh k from 10,000 to 1,073,751,823.
    let mut seed: i64 = 523;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let nums: Vec<i64> = (0..100000).map(|_| 1 + next_random(&mut seed) % 20000).collect();
        arrays.push(nums);
    }
    let mut yes = 0;
    let mut checksum: i64 = 0;
    for round in 0..10i64 {
        for (a, nums) in arrays.iter().enumerate() {
            let high = next_random(&mut seed);
            let k = 10000 + high * 32768 + next_random(&mut seed);
            if check_subarray_sum(nums, k) {
                yes += 1;
                checksum = (checksum + (round + 1) * (a as i64 + 1)) % 1000000007;
            }
        }
    }
    println!("20 arrays of 100000, 10 rounds: {} true, checksum {}", yes, checksum);
}
