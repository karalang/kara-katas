// LeetCode #2044: Count Number of Maximum Bitwise-OR Subsets -- the ★ arm
// in Rust, the same algorithm and workload as subsets.kara: the target is
// the OR of every value, and a take-or-skip search counts the subsets that
// reach it.

fn count_from(nums: &[i64], i: usize, acc: i64, target: i64) -> i64 {
    if i == nums.len() {
        return if acc == target { 1 } else { 0 };
    }
    count_from(nums, i + 1, acc | nums[i], target) + count_from(nums, i + 1, acc, target)
}

fn count_max_or_subsets(nums: &[i64]) -> i64 {
    let target = nums.iter().fold(0, |acc, &x| acc | x);
    count_from(nums, 0, 0, target)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2044i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for r in 0..2000 {
        let top = [100000, 1024, 16, 2][r % 4];
        arrays.push((0..16).map(|_| next_random(&mut seed) % top + 1).collect());
    }
    let mut calls = 0i64;
    let mut sum = 0i64;
    let mut check = 0i64;
    for nums in &arrays {
        let answer = count_max_or_subsets(nums);
        calls += 1;
        sum += answer;
        check = (check * 31 + answer) % 1000000007;
    }
    println!("{} calls: sum {}, checksum {}", calls, sum, check);
}
