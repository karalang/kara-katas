// LeetCode #1800: Maximum Ascending Subarray Sum -- the bench in Rust: the
// ★ arm over 4000 random lists of 100 numbers built once, 400000 calls.

fn max_ascending_sum(nums: &[i32]) -> i32 {
    let mut run = nums[0];
    let mut best = run;
    for i in 1..nums.len() {
        if nums[i] > nums[i - 1] {
            run += nums[i];
        } else {
            run = nums[i];
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
    let mut seed = 1800;
    let mut lists: Vec<Vec<i32>> = Vec::new();
    for _ in 0..4000 {
        let nums: Vec<i32> = (0..100).map(|_| (1 + next_random(&mut seed) % 100) as i32).collect();
        lists.push(nums);
    }
    let mut check: i64 = 0;
    for call in 0..400000i64 {
        let nums = &lists[((check + call) % 4000) as usize];
        check = (check * 31 + max_ascending_sum(nums) as i64) % 1000000007;
    }
    println!("400000 calls over 4000 lists of 100 numbers: checksum {}", check);
}
