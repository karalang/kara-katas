// LeetCode #862: Shortest Subarray with Sum at Least K -- Rust mirror of
// the bench program (the ★ arm, prefix sums and a deque of candidate
// starts).
use std::collections::VecDeque;

fn shortest_subarray(nums: &[i64], k: i64) -> i64 {
    let n = nums.len();
    let mut p: Vec<i64> = vec![0];
    for &x in nums {
        p.push(p[p.len() - 1] + x);
    }
    let mut best = n + 1;
    let mut starts: VecDeque<usize> = VecDeque::new();
    for j in 0..n + 1 {
        while let Some(&i) = starts.front() {
            if p[j] - p[i] >= k {
                best = best.min(j - i);
                starts.pop_front();
            } else {
                break;
            }
        }
        while let Some(&i) = starts.back() {
            if p[i] >= p[j] {
                starts.pop_back();
            } else {
                break;
            }
        }
        starts.push_back(j);
    }
    if best <= n { best as i64 } else { -1 }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_value(seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    let lo = next_random(seed);
    (hi * 32768 + lo) % 200001 - 100000
}

fn main() {
    let n: i64 = 100000;
    let k: i64 = 5000000;
    let rounds = 300;
    let mut seed: i64 = 862;
    let mut nums: Vec<i64> = Vec::new();
    for _ in 0..n {
        nums.push(random_value(&mut seed));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        let hi = next_random(&mut seed);
        let lo = next_random(&mut seed);
        let i = ((hi * 32768 + lo) % n) as usize;
        let old = nums[i];
        nums[i] = random_value(&mut seed);
        let got = shortest_subarray(&nums, k);
        nums[i] = old;
        total += got;
        check = (check * 31 + got + 2) % 1000000007;
    }
    println!("{} rounds on {} values, k = {}: lengths sum to {}, checksum {}", rounds, n, k, total, check);
}
