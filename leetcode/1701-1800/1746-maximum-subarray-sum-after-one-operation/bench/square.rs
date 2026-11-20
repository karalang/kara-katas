// LeetCode #1746: Maximum Subarray Sum After One Operation -- the bench
// (square.kara in Rust): Kadane's scan with two states.

fn max_sum_after_operation(nums: &[i32]) -> i32 {
    let mut plain: i32 = 0;
    let mut squared: i32 = 0;
    let mut best = i32::MIN;
    for &x in nums.iter() {
        squared = (squared + x).max(plain.max(0) + x * x);
        plain = plain.max(0) + x;
        best = best.max(squared);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 20;
    let rounds: i64 = 40;
    let n = 100000;
    let mut seed: i64 = 1746;
    let arrays: Vec<Vec<i32>> = (0..count).map(|_| (0..n).map(|_| (next_random(&mut seed) % 20001 - 10000) as i32).collect()).collect();
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for nums in arrays.iter() {
            let answer = max_sum_after_operation(nums) as i64;
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{} arrays of {} values, {} rounds: sums add to {}, checksum {}", count, n, rounds, sum, check);
}
