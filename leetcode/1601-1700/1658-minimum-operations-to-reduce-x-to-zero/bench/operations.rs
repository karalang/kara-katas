// LeetCode #1658: Minimum Operations to Reduce X to Zero -- the bench's
// Rust mirror: the ★ arm on 1000 random arrays of 100000 numbers from 1 to
// 10000, each x a random prefix plus a random suffix of its array, all
// drawn first.

fn min_operations(nums: &[i32], x: i32) -> i32 {
    let total: i64 = nums.iter().map(|&v| v as i64).sum();
    let target = total - x as i64;
    if target < 0 {
        return -1;
    }
    let n = nums.len() as i64;
    let mut longest: i64 = -1;
    let mut sum: i64 = 0;
    let mut left: usize = 0;
    for right in 0..nums.len() {
        sum += nums[right] as i64;
        while sum > target {
            sum -= nums[left] as i64;
            left += 1;
        }
        if sum == target {
            longest = longest.max((right - left + 1) as i64);
        }
    }
    if longest < 0 { -1 } else { (n - longest) as i32 }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1658;
    let n: usize = 100000;
    let mut problems: Vec<(Vec<i32>, i32)> = Vec::new();
    for _ in 0..1000 {
        let nums: Vec<i32> = (0..n).map(|_| (next_random(&mut seed) % 10000 + 1) as i32).collect();
        let left = (next_random(&mut seed) % 1000) as usize;
        let right = (next_random(&mut seed) % 1000) as usize;
        let mut x: i64 = 0;
        for i in 0..left {
            x += nums[i] as i64;
        }
        for i in n - right..n {
            x += nums[i] as i64;
        }
        problems.push((nums, x.max(1) as i32));
    }
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for (nums, x) in &problems {
        let answer = min_operations(nums, *x) as i64;
        total += answer;
        check = (check * 31 + answer + 2) % 1000000007;
    }
    println!("1000 arrays of 100000 numbers: operations sum to {}, checksum {}", total, check);
}
