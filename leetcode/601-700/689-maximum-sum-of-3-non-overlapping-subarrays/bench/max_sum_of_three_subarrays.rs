// LeetCode #689: Maximum Sum of 3 Non-Overlapping Subarrays -- best to
// each side. Bench.
//
// 100 arrays of 20,000 values from 1 to 65535, each with a k from 1 to
// 1,000, are built once; then 20 rounds answer every array.

fn max_sum_of_three_subarrays(nums: &[i64], k: i64) -> Vec<i64> {
    let n = nums.len() as i64;
    let count = n - k + 1;
    let mut w = vec![0i64; count as usize];
    let mut sum = 0;
    for i in 0..n {
        sum += nums[i as usize];
        if i >= k {
            sum -= nums[(i - k) as usize];
        }
        if i >= k - 1 {
            w[(i - k + 1) as usize] = sum;
        }
    }
    let mut left = vec![0i64; count as usize];
    let mut best = 0i64;
    for i in 0..count {
        if w[i as usize] > w[best as usize] {
            best = i;
        }
        left[i as usize] = best;
    }
    let mut right = vec![0i64; count as usize];
    best = count - 1;
    let mut i = count - 1;
    while i >= 0 {
        if w[i as usize] >= w[best as usize] {
            best = i;
        }
        right[i as usize] = best;
        i -= 1;
    }
    let mut answer: Vec<i64> = Vec::new();
    let mut top = -1;
    for j in k..count - k {
        let a = left[(j - k) as usize];
        let c = right[(j + k) as usize];
        let total = w[a as usize] + w[j as usize] + w[c as usize];
        if total > top {
            top = total;
            answer = vec![a, j, c];
        }
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count: i64 = 100;
    let rounds: i64 = 20;
    let mut seed: i64 = 689;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    let mut ks: Vec<i64> = Vec::new();
    for _ in 0..count {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..20000 {
            nums.push(1 + next_random(&mut seed) % 65535);
        }
        arrays.push(nums);
        ks.push(1 + next_random(&mut seed) % 1000);
    }
    let mut sum: i64 = 0;
    for r in 0..rounds {
        for c in 0..count as usize {
            let got = max_sum_of_three_subarrays(&arrays[c], ks[c]);
            sum = (sum * 31 + got[0] + got[1] + got[2] + r) % 1000000007;
        }
    }
    println!("{} arrays answered, checksum {}", count * rounds, sum);
}
