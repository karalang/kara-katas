// LeetCode #2016: Maximum Difference Between Increasing Elements -- the ★
// arm's benchmark, a mirror of difference.kara.

fn maximum_difference(nums: &[i64]) -> i64 {
    let mut smallest = nums[0];
    let mut best = -1;
    for &x in &nums[1..] {
        if x > smallest {
            best = best.max(x - smallest);
        }
        smallest = smallest.min(x);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2016i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for a in 0..1000i64 {
        let fall = a % 11;
        let mut nums: Vec<i64> = Vec::new();
        for i in 0..10000usize {
            if i > 0 && next_random(&mut seed) % 10 < fall {
                let step = next_random(&mut seed) % 1000;
                nums.push((nums[i - 1] - step).max(1));
            } else {
                let hi = next_random(&mut seed);
                nums.push((hi * 32768 + next_random(&mut seed)) % 1000000000 + 1);
            }
        }
        arrays.push(nums);
    }
    let (mut calls, mut sum, mut check) = (0i64, 0i64, 0i64);
    for _ in 0..10 {
        for nums in &arrays {
            let answer = maximum_difference(nums);
            calls += 1;
            sum += answer;
            check = (check * 31 + answer + 1) % 1000000007;
        }
    }
    println!("{calls} calls: sum {sum}, checksum {check}");
}
