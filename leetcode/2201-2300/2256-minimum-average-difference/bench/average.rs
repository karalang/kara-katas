// LeetCode #2256: Minimum Average Difference -- the benchmark's Rust
// mirror of average.kara: one pass with the total known, the first index
// whose two rounded-down averages are nearest.

fn minimum_average_difference(nums: &[i64]) -> i64 {
    let n = nums.len() as i64;
    let total: i64 = nums.iter().sum();
    let mut left = 0i64;
    let mut best = 0i64;
    let mut best_gap = -1i64;
    for i in 0..n {
        left += nums[i as usize];
        let right = total - left;
        let left_average = left / (i + 1);
        let right_average = if i + 1 == n { 0 } else { right / (n - i - 1) };
        let gap = (left_average - right_average).abs();
        if best_gap < 0 || gap < best_gap {
            best_gap = gap;
            best = i;
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2256i64;
    let mut check = 0i64;
    for _ in 0..20 {
        let nums: Vec<i64> = (0..100000).map(|_| wide_random(&mut seed) % 100001).collect();
        check = (check * 31 + minimum_average_difference(&nums) + 1) % 1000000007;
    }
    println!("20 cases of 10^5 values: checksum {}", check);
}
