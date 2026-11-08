// LeetCode #2031: Count Subarrays With More Ones Than Zeros -- the ★ arm in
// Rust, the same algorithm and workload as subarrays.kara.

const MOD: i64 = 1_000_000_007;

fn subarrays_more_ones(nums: &[i64]) -> i64 {
    let n = nums.len();
    let mut seen = vec![0i64; 2 * n + 1];
    let mut prefix = n;
    seen[prefix] = 1;
    let mut below: i64 = 0;
    let mut total: i64 = 0;
    for &x in nums {
        if x == 1 {
            below += seen[prefix];
            prefix += 1;
        } else {
            prefix -= 1;
            below -= seen[prefix];
        }
        total = (total + below) % MOD;
        seen[prefix] += 1;
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2031;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for a in 0..20i64 {
        let nums: Vec<i64> = (0..100000)
            .map(|_| if next_random(&mut seed) % 10 < a % 9 + 1 { 1 } else { 0 })
            .collect();
        arrays.push(nums);
    }
    let (mut calls, mut sum, mut check) = (0i64, 0i64, 0i64);
    for round in 0..100usize {
        for a in 0..20usize {
            let at = (round * 997 + a * 31) % 100000;
            arrays[a][at] = 1 - arrays[a][at];
            let answer = subarrays_more_ones(&arrays[a]);
            calls += 1;
            sum = (sum + answer) % MOD;
            check = (check * 31 + answer) % MOD;
        }
    }
    println!("{} calls: sum {}, checksum {}", calls, sum, check);
}
