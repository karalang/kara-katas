// LeetCode #2765: Longest Alternating Subarray -- the bench
// (alternating.kara in Rust): one pass with the length of the alternating
// run ending at each number.

fn alternating_subarray(nums: &[i64]) -> i64 {
    let mut best = -1;
    let mut run = 1;
    for i in 1..nums.len() {
        if run >= 2 && nums[i] == nums[i - 2] {
            run += 1;
        } else if nums[i] - nums[i - 1] == 1 {
            run = 2;
        } else {
            run = 1;
        }
        if run >= 2 {
            best = best.max(run);
        }
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
    let mut seed = 2765;
    let mut cases: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let top = next_random(&mut seed) % 4 + 2;
        let nums: Vec<i64> = (0..100).map(|_| next_random(&mut seed) % top + 1).collect();
        cases.push(nums);
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for nums in cases.iter() {
            let length = alternating_subarray(nums);
            sum += length;
            check = (check * 31 + length + 1 + r) % 1000000007;
        }
    }
    println!("{count} arrays of 100, {rounds} rounds: lengths sum to {sum}, checksum {check}");
}
