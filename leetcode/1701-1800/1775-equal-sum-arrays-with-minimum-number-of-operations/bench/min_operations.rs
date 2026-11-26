// LeetCode #1775: Equal Sum Arrays With Minimum Number of Operations --
// the bench in Rust, mirroring min_operations.kara: the gains counted by
// size and the largest taken first.
fn min_operations(nums1: &[i32], nums2: &[i32]) -> i32 {
    let sum1: i32 = nums1.iter().sum();
    let sum2: i32 = nums2.iter().sum();
    if sum1 == sum2 {
        return 0;
    }
    let (low, high) = if sum1 < sum2 { (nums1, nums2) } else { (nums2, nums1) };
    let mut gap = (sum1 - sum2).abs();
    let mut gains = vec![0i32; 6];
    for &x in low {
        gains[(6 - x) as usize] += 1;
    }
    for &x in high {
        gains[(x - 1) as usize] += 1;
    }
    let mut ops = 0;
    for g in (1..6).rev() {
        while gains[g] > 0 && gap > 0 {
            gap -= g as i32;
            gains[g] -= 1;
            ops += 1;
        }
    }
    if gap > 0 { -1 } else { ops }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1775;
    let mut lists: Vec<Vec<i32>> = Vec::new();
    for _ in 0..40 {
        let low = 1 + next_random(&mut seed) % 3;
        let high = 4 + next_random(&mut seed) % 3;
        lists.push((0..100000).map(|_| (low + next_random(&mut seed) % (high - low + 1)) as i32).collect());
    }
    let mut check: i64 = 0;
    for call in 0..400i64 {
        let a = ((check + call) % 40) as usize;
        let b = ((check / 40 + call * 7) % 40) as usize;
        check = (check * 31 + min_operations(&lists[a], &lists[b]) as i64 + 1) % 1000000007;
    }
    println!("400 calls over 40 lists: checksum {}", check);
}
