// LeetCode #1031: Maximum Sum of Two Non-Overlapping Subarrays -- bench
// Mirrors ./max_two.kara; see ../README.md § Benchmarks.

fn max_sum_two_no_overlap(nums: &[i64], first_len: usize, second_len: usize) -> i64 {
    let n = nums.len();
    let mut prefix: Vec<i64> = vec![0; n + 1];
    for i in 0..n {
        prefix[i + 1] = prefix[i] + nums[i];
    }
    let mut best = 0;
    let mut best_first = 0;
    let mut best_second = 0;
    for i in first_len + second_len..n + 1 {
        best_first = i64::max(best_first, prefix[i - second_len] - prefix[i - second_len - first_len]);
        best_second = i64::max(best_second, prefix[i - first_len] - prefix[i - first_len - second_len]);
        best = best
            .max(best_first + prefix[i] - prefix[i - second_len])
            .max(best_second + prefix[i] - prefix[i - first_len]);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 1000;
    let rounds = 200;
    let mut seed = 1031;
    let mut cases: Vec<(Vec<i64>, usize, usize)> = Vec::new();
    for _ in 0..count {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..1000 {
            nums.push(next_random(&mut seed) % 1001);
        }
        let first_len = (next_random(&mut seed) % 999 + 1) as usize;
        let second_len = (next_random(&mut seed) % (1000 - first_len as i64) + 1) as usize;
        cases.push((nums, first_len, second_len));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        for (nums, first_len, second_len) in cases.iter() {
            let answer = max_sum_two_no_overlap(nums, *first_len, *second_len);
            total += answer;
            check = (check * 131 + answer) % 1000000007;
        }
    }
    println!("{} arrays of 1000 values, {} rounds: sum {}, checksum {}", count, rounds, total, check);
}
