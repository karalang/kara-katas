// LeetCode #2760: Longest Even Odd Subarray With Threshold -- the bench
// (threshold.kara in Rust): one pass with the length of the good run
// ending at each number.

fn longest_alternating_subarray(nums: &[i64], threshold: i64) -> i64 {
    let mut best = 0;
    let mut run = 0;
    for i in 0..nums.len() {
        let x = nums[i];
        if x > threshold {
            run = 0;
        } else if run > 0 && x % 2 != nums[i - 1] % 2 {
            run += 1;
        } else if x % 2 == 0 {
            run = 1;
        } else {
            run = 0;
        }
        best = best.max(run);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 100000;
    let rounds = 10;
    let mut seed = 2760;
    let mut cases: Vec<(Vec<i64>, i64)> = Vec::new();
    for _ in 0..count {
        let nums: Vec<i64> = (0..100).map(|_| next_random(&mut seed) % 100 + 1).collect();
        let threshold = next_random(&mut seed) % 100 + 1;
        cases.push((nums, threshold));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (nums, threshold) in cases.iter() {
            let length = longest_alternating_subarray(nums, *threshold);
            sum += length;
            check = (check * 31 + length + r) % 1000000007;
        }
    }
    println!("{count} arrays of 100, {rounds} rounds: lengths sum to {sum}, checksum {check}");
}
