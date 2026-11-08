// LeetCode #1509: Minimum Difference Between Largest and Smallest Value in
// Three Moves -- the bench: 20 arrays of 100000 numbers built once, then
// each answered five times by the ★ arm.

fn min_difference(nums: &[i64]) -> i64 {
    let n = nums.len();
    if n <= 4 {
        return 0;
    }
    let mut sorted = nums.to_vec();
    sorted.sort();
    let mut best = sorted[n - 1] - sorted[0];
    for low in 0..4 {
        best = best.min(sorted[n - 4 + low] - sorted[low]);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1509;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let mut nums = Vec::new();
        for _ in 0..100000 {
            let wide = next_random(&mut seed) * 32768 + next_random(&mut seed);
            nums.push(wide % 2000000001 - 1000000000);
        }
        arrays.push(nums);
    }
    let mut check: i64 = 0;
    for _ in 0..5 {
        for nums in &arrays {
            check = (check * 31 + min_difference(nums) % 1000000007 + 1) % 1000000007;
        }
    }
    println!("100 answers over 20 arrays of 100000 numbers: checksum {}", check);
}
