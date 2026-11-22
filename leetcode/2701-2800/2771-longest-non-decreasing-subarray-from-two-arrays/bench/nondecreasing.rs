// LeetCode #2771: Longest Non-decreasing Subarray From Two Arrays -- the
// bench in Rust: the ★ arm over 20 pairs of 10^5 numbers, all drawn
// first, then each answered 10 times.

fn max_non_decreasing_length(nums1: &[i64], nums2: &[i64]) -> i64 {
    let n = nums1.len();
    let (mut one, mut two) = (1i64, 1i64);
    let mut best = 1;
    for i in 1..n {
        let mut next_one = 1;
        let mut next_two = 1;
        if nums1[i - 1] <= nums1[i] {
            next_one = next_one.max(one + 1);
        }
        if nums2[i - 1] <= nums1[i] {
            next_one = next_one.max(two + 1);
        }
        if nums1[i - 1] <= nums2[i] {
            next_two = next_two.max(one + 1);
        }
        if nums2[i - 1] <= nums2[i] {
            next_two = next_two.max(two + 1);
        }
        one = next_one;
        two = next_two;
        best = best.max(one).max(two);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn main() {
    let count = 20;
    let rounds = 10;
    let n: i64 = 100000;
    let mut seed: i64 = 2771;
    let mut pairs: Vec<(Vec<i64>, Vec<i64>)> = Vec::new();
    for _ in 0..count {
        let noise = next_random(&mut seed) % 200 + 1;
        let nums1: Vec<i64> = (0..n).map(|i| i * 10 + next_random(&mut seed) % noise + 1).collect();
        let nums2: Vec<i64> = (0..n).map(|_| wide(&mut seed) % 1000000000 + 1).collect();
        pairs.push((nums1, nums2));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (nums1, nums2) in pairs.iter() {
            let a = max_non_decreasing_length(nums1, nums2);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    println!("{} pairs of 10^5, {} rounds: lengths sum to {}, checksum {}", count, rounds, total, check);
}
