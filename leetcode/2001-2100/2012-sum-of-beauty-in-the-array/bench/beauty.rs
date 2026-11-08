// LeetCode #2012: Sum of Beauty in the Array -- the ★ arm's benchmark, a
// mirror of beauty.kara.

fn sum_of_beauties(nums: &[i64]) -> i64 {
    let n = nums.len();
    let mut min_after = vec![0i64; n];
    min_after[n - 1] = nums[n - 1];
    for i in (0..n - 1).rev() {
        min_after[i] = min_after[i + 1].min(nums[i]);
    }
    let mut max_before = nums[0];
    let mut total = 0;
    for i in 1..n - 1 {
        if max_before < nums[i] && nums[i] < min_after[i + 1] {
            total += 2;
        } else if nums[i - 1] < nums[i] && nums[i] < nums[i + 1] {
            total += 1;
        }
        max_before = max_before.max(nums[i]);
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2012i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for a in 0..1000 {
        let rise = a % 11;
        let mut nums: Vec<i64> = Vec::new();
        for i in 0..2000 {
            if i > 0 && next_random(&mut seed) % 10 < rise {
                let v = (nums[i - 1] + next_random(&mut seed) % 3 + 1).min(100000);
                nums.push(v);
            } else {
                nums.push(next_random(&mut seed) % 100000 + 1);
            }
        }
        arrays.push(nums);
    }
    let (mut calls, mut sum, mut check) = (0i64, 0i64, 0i64);
    for _ in 0..5 {
        for nums in &arrays {
            let answer = sum_of_beauties(nums);
            calls += 1;
            sum += answer;
            check = (check * 31 + answer) % 1000000007;
        }
    }
    println!("{calls} calls: sum {sum}, checksum {check}");
}
