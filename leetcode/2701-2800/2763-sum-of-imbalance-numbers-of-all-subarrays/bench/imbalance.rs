// LeetCode #2763: Sum of Imbalance Numbers of All Subarrays -- the bench
// (imbalance.kara in Rust): each index counted for the subarrays in which
// it is the leftmost occurrence of a run's top value, from the last x or
// x + 1 before it and the first x + 1 after it.

fn sum_imbalance_numbers(nums: &[i64]) -> i64 {
    let n = nums.len() as i64;
    let mut left: Vec<i64> = vec![0; n as usize];
    let mut last: Vec<i64> = vec![-1; n as usize + 2];
    for (i, &x) in nums.iter().enumerate() {
        left[i] = last[x as usize].max(last[x as usize + 1]);
        last[x as usize] = i as i64;
    }
    let mut first: Vec<i64> = vec![n; n as usize + 2];
    let mut total = 0;
    for i in (0..n).rev() {
        let x = nums[i as usize] as usize;
        total += (i - left[i as usize]) * (first[x + 1] - i);
        first[x] = i;
    }
    total - n * (n + 1) / 2
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 20000;
    let rounds = 5;
    let mut seed = 2763;
    let mut cases: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let nums: Vec<i64> = (0..1000).map(|_| next_random(&mut seed) % 1000 + 1).collect();
        cases.push(nums);
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for nums in cases.iter() {
            let found = sum_imbalance_numbers(nums);
            sum += found;
            check = (check * 31 + found + r) % 1000000007;
        }
    }
    println!("{count} arrays of 1000, {rounds} rounds: imbalances sum to {sum}, checksum {check}");
}
