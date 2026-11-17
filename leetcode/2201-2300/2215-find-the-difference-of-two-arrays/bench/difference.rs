// LeetCode #2215: Find the Difference of Two Arrays -- bench mirror of
// difference.kara: each array put in a hash set, and each list the
// numbers of one set the other lacks.
use std::collections::HashSet;

fn find_difference(nums1: &[i64], nums2: &[i64]) -> Vec<Vec<i64>> {
    let first: HashSet<i64> = nums1.iter().copied().collect();
    let second: HashSet<i64> = nums2.iter().copied().collect();
    let only_first: Vec<i64> = first.iter().copied().filter(|x| !second.contains(x)).collect();
    let only_second: Vec<i64> = second.iter().copied().filter(|x| !first.contains(x)).collect();
    vec![only_first, only_second]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2215;
    let mut pairs: Vec<(Vec<i64>, Vec<i64>)> = Vec::new();
    for p in 0..200 {
        // 1000 numbers each, spread over -30..30, -300..300 and -1000..1000
        let spread = [30, 300, 1000][p % 3];
        let nums1: Vec<i64> = (0..1000).map(|_| next_random(&mut seed) % (2 * spread + 1) - spread).collect();
        let nums2: Vec<i64> = (0..1000).map(|_| next_random(&mut seed) % (2 * spread + 1) - spread).collect();
        pairs.push((nums1, nums2));
    }
    let mut check: i64 = 0;
    for p in 0..200 {
        for r in 0..10 {
            // punch: one number of the first array moves before each answer
            let at = r * 97;
            pairs[p].0[at] = (pairs[p].0[at] + 1001) % 2001 - 1000;
            let answer = find_difference(&pairs[p].0, &pairs[p].1);
            for list in &answer {
                // the lists come in any order: their lengths and sums do not
                check = (check * 31 + list.len() as i64) % 1000000007;
                check = (check * 31 + list.iter().sum::<i64>() + 1000000) % 1000000007;
            }
        }
    }
    println!("200 pairs of 1000, 10 punches: checksum {check}");
}
