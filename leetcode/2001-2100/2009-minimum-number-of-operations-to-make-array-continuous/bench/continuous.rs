// LeetCode #2009: Minimum Number of Operations to Make Array Continuous --
// the ★ arm's benchmark, a mirror of continuous.kara.

fn min_operations(nums: &[i64]) -> i64 {
    let n = nums.len() as i64;
    let mut values = nums.to_vec();
    values.sort();
    values.dedup();
    let mut kept = 0usize;
    let mut right = 0usize;
    for left in 0..values.len() {
        while right < values.len() && values[right] <= values[left] + n - 1 {
            right += 1;
        }
        kept = kept.max(right - left);
    }
    n - kept as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2009i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for a in 0..200i64 {
        let top = 2000 * (a + 1);
        let mut nums = Vec::new();
        for _ in 0..2000 {
            let hi = next_random(&mut seed);
            nums.push((hi * 32768 + next_random(&mut seed)) % top + 1);
        }
        arrays.push(nums);
    }
    let (mut calls, mut sum, mut check) = (0i64, 0i64, 0i64);
    for _ in 0..25 {
        for nums in &arrays {
            let answer = min_operations(nums);
            calls += 1;
            sum += answer;
            check = (check * 31 + answer) % 1000000007;
        }
    }
    println!("{calls} calls: sum {sum}, checksum {check}");
}
