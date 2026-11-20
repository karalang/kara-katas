// LeetCode #1708: Largest Subarray Length K -- the Rust mirror of the
// bench (largest.kara): the largest first value among the starts that
// leave room for k, on 50 random arrays of 100000 distinct values, each
// answered 100 times.

fn largest_subarray(nums: &[i32], k: usize) -> Vec<i32> {
    let mut best = 0;
    for i in 1..=nums.len() - k {
        if nums[i] > nums[best] {
            best = i;
        }
    }
    nums[best..best + k].to_vec()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 50;
    let rounds: i64 = 100;
    let n: i64 = 100000;
    let mut seed: i64 = 1708;
    let mut problems: Vec<(Vec<i32>, usize)> = Vec::new();
    for _ in 0..count {
        let mut nums: Vec<i32> = (0..n).map(|v| v as i32).collect();
        for i in (1..n).rev() {
            let a = next_random(&mut seed);
            let j = (a * 32768 + next_random(&mut seed)) % (i + 1);
            nums.swap(i as usize, j as usize);
        }
        for i in 0..n as usize {
            nums[i] = nums[i] * 10000 + (next_random(&mut seed) % 10000) as i32;
        }
        let a = next_random(&mut seed);
        let k = (a * 32768 + next_random(&mut seed)) % n + 1;
        problems.push((nums, k as usize));
    }
    let mut chosen: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (nums, k) in problems.iter() {
            let answer = largest_subarray(nums, *k);
            let len = answer.len() as i64;
            chosen += len;
            check = (check * 31 + len + answer[0] as i64 + answer[answer.len() - 1] as i64 + r) % 1000000007;
        }
    }
    println!("{count} arrays of {n} values, {rounds} rounds: {chosen} chosen, checksum {check}");
}
