// LeetCode #1755: Closest Subsequence Sum -- the bench (closest.kara in
// Rust): meet in the middle with binary search.

fn subset_sums(values: &[i32]) -> Vec<i32> {
    let count = 1usize << values.len();
    let mut sums: Vec<i32> = vec![0; count];
    for mask in 1..count {
        sums[mask] = sums[mask & (mask - 1)] + values[mask.trailing_zeros() as usize];
    }
    sums
}

fn min_abs_difference(nums: &[i32], goal: i32) -> i32 {
    let half = nums.len() / 2;
    let left = subset_sums(&nums[..half]);
    let mut right = subset_sums(&nums[half..]);
    right.sort();
    let mut best = i32::MAX;
    for &l in left.iter() {
        let rest = goal - l;
        let at = right.partition_point(|&r| r < rest);
        if at < right.len() {
            best = best.min(right[at] - rest);
        }
        if at > 0 {
            best = best.min(rest - right[at - 1]);
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    next_random(seed) * 32768 + next_random(seed)
}

fn main() {
    let count = 8;
    let n = 40;
    let mut seed: i64 = 1755;
    let mut problems: Vec<(Vec<i32>, i32)> = Vec::new();
    for _ in 0..count {
        let nums: Vec<i32> = (0..n).map(|_| (wide(&mut seed) % 20000001 - 10000000) as i32).collect();
        let goal = (wide(&mut seed) % 200000001 - 100000000) as i32;
        problems.push((nums, goal));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for (nums, goal) in problems.iter() {
        let answer = min_abs_difference(nums, *goal) as i64;
        sum += answer;
        check = (check * 31 + answer) % 1000000007;
    }
    println!("{} problems of {} values: differences add to {}, checksum {}", count, n, sum, check);
}
