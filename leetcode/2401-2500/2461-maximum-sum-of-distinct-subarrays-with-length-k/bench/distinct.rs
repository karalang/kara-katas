// LeetCode #2461: Maximum Sum of Distinct Subarrays With Length K -- the
// bench, the ★ arm in Rust: a sliding window of `k` with a `HashMap`
// counting each value in it and the window's sum.
use std::collections::HashMap;

fn maximum_subarray_sum(nums: &[i64], k: usize) -> i64 {
    let mut count: HashMap<i64, i64> = HashMap::new();
    let mut sum = 0;
    let mut best = 0;
    for i in 0..nums.len() {
        *count.entry(nums[i]).or_insert(0) += 1;
        sum += nums[i];
        if i >= k {
            let out = nums[i - k];
            let c = count.get_mut(&out).unwrap();
            *c -= 1;
            if *c == 0 {
                count.remove(&out);
            }
            sum -= out;
        }
        if i + 1 >= k && count.len() == k {
            best = best.max(sum);
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 10 arrays of 10^5 values from 1 to 2000 built once; then 28
    // passes, each setting one value of every array from the checksum so
    // far, then answering every array with k = 5 + 7 p % 40, folding the
    // answer plus the pass into the checksum
    let mut seed = 2461;
    let mut arrays: Vec<Vec<i64>> = (0..10).map(|_| (0..100000).map(|_| 1 + next_random(&mut seed) % 2000).collect()).collect();
    let mut check = 0i64;
    for p in 0..28i64 {
        let k = (5 + 7 * p % 40) as usize;
        for a in 0..arrays.len() {
            arrays[a][((check + a as i64) % 100000) as usize] = 1 + check % 2000;
            check = (check * 31 + maximum_subarray_sum(&arrays[a], k) + p) % 1000000007;
        }
    }
    println!("28 passes over 10 arrays of 10^5: checksum {check}");
}
