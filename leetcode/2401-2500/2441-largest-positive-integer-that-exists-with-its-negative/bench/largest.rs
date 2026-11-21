// LeetCode #2441: Largest Positive Integer That Exists With Its Negative
// -- the bench, the ★ arm: a table of 2001 flags, offset by 1000, and
// the largest magnitude whose negative was seen.

fn find_max_k(nums: &[i64]) -> i64 {
    let mut seen = vec![false; 2001];
    let mut best = -1i64;
    for &x in nums {
        if seen[(1000 - x) as usize] {
            best = best.max(x.abs());
        }
        seen[(1000 + x) as usize] = true;
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn nonzero(seed: &mut i64) -> i64 {
    let v = 1 + next_random(seed) % 1000;
    if next_random(seed) % 2 == 0 { v } else { -v }
}

fn main() {
    let mut seed = 2441i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..100 {
        let mut nums = Vec::new();
        for _ in 0..1000 {
            nums.push(nonzero(&mut seed));
        }
        arrays.push(nums);
    }
    let mut check = 0i64;
    for p in 0..1000i64 {
        for c in 0..arrays.len() {
            let at = ((p * 7919 + c as i64 * 104729) % 1000) as usize;
            arrays[c][at] = nonzero(&mut seed);
            check = (check * 31 + find_max_k(&arrays[c]) + p) % 1000000007;
        }
    }
    println!("1000 passes over 100 arrays of 1000 values: checksum {}", check);
}
