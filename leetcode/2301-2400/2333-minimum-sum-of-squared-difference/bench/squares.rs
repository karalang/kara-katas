// LeetCode #2333: Minimum Sum of Squared Difference -- the bench, the ★
// arm in Rust: the gaps counted by size, the largest dropped a level at
// a time while the moves cover them, and the moves left taking that many
// of the rest one lower.

fn min_sum_square_diff(nums1: &[i64], nums2: &[i64], k1: i64, k2: i64) -> i64 {
    let mut count = vec![0i64; 100001];
    let mut top = 0usize;
    for i in 0..nums1.len() {
        let gap = (nums1[i] - nums2[i]).unsigned_abs() as usize;
        count[gap] += 1;
        top = top.max(gap);
    }
    let mut moves = k1 + k2;
    let mut level = top;
    while level > 0 && moves >= count[level] {
        moves -= count[level];
        count[level - 1] += count[level];
        count[level] = 0;
        level -= 1;
    }
    if level > 0 {
        count[level] -= moves;
        count[level - 1] += moves;
    }
    let mut total = 0i64;
    for gap in 1..=level {
        total += count[gap] * (gap as i64) * (gap as i64);
    }
    total
}

fn scrambled(index: i64) -> i64 {
    index * 2654435761 % 2147483647
}

fn main() {
    let mut cases: Vec<(Vec<i64>, Vec<i64>)> = Vec::new();
    for c in 0..10i64 {
        let nums1: Vec<i64> = (0..20000).map(|i| scrambled(c * 40000 + i) % 100001).collect();
        let nums2: Vec<i64> = (0..20000).map(|i| scrambled(c * 40000 + 20000 + i) % 100001).collect();
        cases.push((nums1, nums2));
    }
    let mut check = 0i64;
    for p in 0..10i64 {
        for c in 0..10i64 {
            let (nums1, nums2) = &cases[c as usize];
            let k1 = (10 * c + p) * 3000000 % 400000000;
            let k2 = (7 * p + c) * 5000000 % 300000000;
            check = (check * 31 + min_sum_square_diff(nums1, nums2, k1, k2)) % 1000000007;
        }
    }
    println!("10 passes over 10 cases of 2*10^4 pairs: checksum {}", check);
}
