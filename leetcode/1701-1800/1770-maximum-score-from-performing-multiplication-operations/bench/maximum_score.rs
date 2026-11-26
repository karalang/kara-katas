// LeetCode #1770: Maximum Score from Performing Multiplication Operations
// -- the bench in Rust, mirroring maximum_score.kara: one row of the table,
// filled from the last operation back to the first.
fn maximum_score(nums: &[i32], multipliers: &[i32]) -> i32 {
    let n = nums.len();
    let m = multipliers.len();
    let mut best = vec![0i32; m + 1];
    for i in (0..m).rev() {
        for left in 0..i + 1 {
            let right = n - 1 - (i - left);
            let take_left = multipliers[i] * nums[left] + best[left + 1];
            let take_right = multipliers[i] * nums[right] + best[left];
            best[left] = take_left.max(take_right);
        }
    }
    best[0]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_numbers(seed: &mut i64, n: usize) -> Vec<i32> {
    (0..n).map(|_| (next_random(seed) % 2001 - 1000) as i32).collect()
}

fn main() {
    let mut seed: i64 = 1770;
    let numbers: Vec<Vec<i32>> = (0..100).map(|_| random_numbers(&mut seed, 1000)).collect();
    let weights: Vec<Vec<i32>> = (0..100).map(|_| random_numbers(&mut seed, 300)).collect();
    let mut check: i64 = 0;
    for call in 0..2000i64 {
        let score = maximum_score(&numbers[((check + call * 7919) % 100) as usize], &weights[((check / 100 + call) % 100) as usize]);
        check = (check * 31 + score as i64 % 1000000007 + 1000000007) % 1000000007;
    }
    println!("2000 calls over 100 lists: checksum {}", check);
}
