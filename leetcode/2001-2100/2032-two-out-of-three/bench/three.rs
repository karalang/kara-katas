// LeetCode #2032: Two Out of Three -- the ★ arm in Rust, the same
// algorithm and workload as three.kara.

fn two_out_of_three(nums1: &[i64], nums2: &[i64], nums3: &[i64]) -> Vec<i64> {
    let mut mask = [0i64; 101];
    for &x in nums1 {
        mask[x as usize] |= 1;
    }
    for &x in nums2 {
        mask[x as usize] |= 2;
    }
    for &x in nums3 {
        mask[x as usize] |= 4;
    }
    let mut out = Vec::new();
    for v in 1..101 {
        if mask[v].count_ones() >= 2 {
            out.push(v as i64);
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2032;
    let mut problems: Vec<Vec<Vec<i64>>> = Vec::new();
    for p in 0..100i64 {
        let mut arrays = Vec::new();
        for _ in 0..3 {
            let nums: Vec<i64> = (0..100).map(|_| next_random(&mut seed) % (p % 90 + 11) + 1).collect();
            arrays.push(nums);
        }
        problems.push(arrays);
    }
    let (mut calls, mut kept, mut check) = (0i64, 0i64, 0i64);
    for round in 0..4000usize {
        for p in 0..100usize {
            let k = (round + p) % 3;
            let at = (round * 7 + p * 13) % 100;
            problems[p][k][at] = (problems[p][k][at] + round as i64) % 100 + 1;
            let answer = two_out_of_three(&problems[p][0], &problems[p][1], &problems[p][2]);
            calls += 1;
            kept += answer.len() as i64;
            for v in answer {
                check = (check * 31 + v) % 1000000007;
            }
        }
    }
    println!("{} calls: {} values kept, checksum {}", calls, kept, check);
}
