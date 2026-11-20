// LeetCode #1749: Maximum Absolute Sum of Any Subarray -- the bench
// (abs.kara in Rust): Kadane's scan both ways.

fn max_absolute_sum(nums: &[i32]) -> i32 {
    let mut high: i32 = 0;
    let mut low: i32 = 0;
    let mut best: i32 = 0;
    for &x in nums.iter() {
        high = high.max(0) + x;
        low = low.min(0) + x;
        best = best.max(high.max(-low));
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
    let mut seed: i64 = 1749;
    let arrays: Vec<Vec<i32>> = (0..count).map(|_| (0..n).map(|_| (next_random(&mut seed) % 20001 - 10000) as i32).collect()).collect();
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for nums in arrays.iter() {
            let answer = max_absolute_sum(nums) as i64;
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{} arrays of {} values, {} rounds: answers add to {}, checksum {}", count, n, rounds, sum, check);
}
