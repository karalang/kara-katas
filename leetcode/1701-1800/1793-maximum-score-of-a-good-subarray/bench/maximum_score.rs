// LeetCode #1793: Maximum Score of a Good Subarray -- the bench in Rust: the
// ★ arm over 200 random lists of 1000 numbers built once, 40000 calls.

fn maximum_score(nums: &[i32], k: i32) -> i32 {
    let n = nums.len() as i64;
    let mut i = k as i64;
    let mut j = k as i64;
    let mut low = nums[i as usize];
    let mut best = low;
    while i > 0 || j < n - 1 {
        let left = if i > 0 { nums[(i - 1) as usize] } else { 0 };
        let right = if j < n - 1 { nums[(j + 1) as usize] } else { 0 };
        if left > right {
            i -= 1;
            low = low.min(left);
        } else {
            j += 1;
            low = low.min(right);
        }
        best = best.max(low * (j - i + 1) as i32);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1793;
    let mut lists: Vec<Vec<i32>> = Vec::new();
    for _ in 0..200 {
        let nums: Vec<i32> = (0..1000).map(|_| (1 + next_random(&mut seed) % 20000) as i32).collect();
        lists.push(nums);
    }
    let mut check: i64 = 0;
    for call in 0..40000i64 {
        let nums = &lists[((check + call) % 200) as usize];
        let k = check % 1000;
        check = (check * 31 + maximum_score(nums, k as i32) as i64) % 1000000007;
    }
    println!("40000 calls over 200 lists of 1000 numbers: checksum {}", check);
}
