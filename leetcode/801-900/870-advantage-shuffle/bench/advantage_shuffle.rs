// LeetCode #870: Advantage Shuffle -- Rust mirror of the bench program
// (the ★ arm, greedy from the largest), with a stable sort of the indices
// as in the Kāra program.

fn advantage_count(nums1: &[i64], nums2: &[i64]) -> Vec<i64> {
    let n = nums1.len();
    let mut sorted = nums1.to_vec();
    sorted.sort();
    let mut order: Vec<usize> = (0..n).collect();
    order.sort_by_key(|&i| -nums2[i]);
    let mut result = vec![0i64; n];
    let mut lo = 0usize;
    let mut hi = n as i64 - 1;
    for &i in &order {
        if sorted[hi as usize] > nums2[i] {
            result[i] = sorted[hi as usize];
            hi -= 1;
        } else {
            result[i] = sorted[lo];
            lo += 1;
        }
    }
    result
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_vec(seed: &mut i64, n: usize) -> Vec<i64> {
    let mut v = Vec::new();
    for _ in 0..n {
        let hi = next_random(seed);
        let lo = next_random(seed);
        v.push((hi * 32768 + lo) % 1000000001);
    }
    v
}

fn main() {
    let mut seed: i64 = 870;
    let mut wins: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..20 {
        let nums1 = random_vec(&mut seed, 100000);
        let nums2 = random_vec(&mut seed, 100000);
        let result = advantage_count(&nums1, &nums2);
        for i in 0..result.len() {
            if result[i] > nums2[i] {
                wins += 1;
            }
            check = (check + result[i] * (i as i64 + 1)) % 1000000007;
        }
    }
    println!("20 pairs of 100000 values: {} wins, checksum {}", wins, check);
}
