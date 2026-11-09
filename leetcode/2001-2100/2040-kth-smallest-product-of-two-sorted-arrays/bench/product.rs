// LeetCode #2040: Kth Smallest Product of Two Sorted Arrays -- the ★ arm in
// Rust, the same algorithm and workload as product.kara: binary search on
// the answer, the products at most `x` counted by `partition_point`.

fn count_at_most(nums1: &[i64], nums2: &[i64], x: i64) -> i64 {
    let mut count = 0i64;
    for &a in nums1 {
        if a > 0 {
            count += nums2.partition_point(|&b| a * b <= x) as i64;
        } else if a < 0 {
            count += (nums2.len() - nums2.partition_point(|&b| a * b > x)) as i64;
        } else if x >= 0 {
            count += nums2.len() as i64;
        }
    }
    count
}

fn kth_smallest_product(nums1: &[i64], nums2: &[i64], k: i64) -> i64 {
    let mut lo: i64 = -10_000_000_000;
    let mut hi: i64 = 10_000_000_000;
    while lo < hi {
        let mid = lo + (hi - lo).div_euclid(2);
        if count_at_most(nums1, nums2, mid) >= k {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    lo
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn sorted_values(n: i64, top: i64, seed: &mut i64) -> Vec<i64> {
    let mut v: Vec<i64> = (0..n)
        .map(|_| {
            let hi = next_random(seed);
            (hi * 32768 + next_random(seed)) % (2 * top + 1) - top
        })
        .collect();
    v.sort();
    v
}

fn main() {
    let mut seed = 2040i64;
    let n = 50000i64;
    let mut pairs: Vec<(Vec<i64>, Vec<i64>)> = Vec::new();
    for r in 0..4 {
        let top = [100000, 3, 1000, 100000][r];
        let a = sorted_values(n, top, &mut seed);
        let b = sorted_values(n, top, &mut seed);
        pairs.push((a, b));
    }
    let mut calls = 0i64;
    let mut sum = 0i64;
    let mut check = 0i64;
    for round in 0..3i64 {
        for r in 0..4usize {
            let k = (round * 4 + r as i64 + 1) * (n * n / 13) + 1;
            let answer = kth_smallest_product(&pairs[r].0, &pairs[r].1, k);
            calls += 1;
            sum += answer;
            check = (check * 31 + answer.rem_euclid(1000000007)) % 1000000007;
        }
    }
    println!("{} calls: sum {}, checksum {}", calls, sum, check);
}
