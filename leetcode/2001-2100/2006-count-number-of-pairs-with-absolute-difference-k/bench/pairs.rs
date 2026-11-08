// LeetCode #2006: Count Number of Pairs With Absolute Difference K -- the
// benchmark's Rust twin, the same algorithm as pairs.kara here.

fn count_k_difference(nums: &[i64], k: i64) -> i64 {
    let mut seen = vec![0i64; 101];
    let mut pairs = 0;
    for &x in nums {
        if x - k >= 1 {
            pairs += seen[(x - k) as usize];
        }
        if x + k <= 100 {
            pairs += seen[(x + k) as usize];
        }
        seen[x as usize] += 1;
    }
    pairs
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 20000 arrays of 200 values up to 100 built once, then the ★ arm on
    // each for 25 rounds, k moving with the round
    let mut seed = 2006i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20000 {
        arrays.push((0..200).map(|_| next_random(&mut seed) % 100 + 1).collect());
    }
    let (mut calls, mut sum, mut check) = (0i64, 0i64, 0i64);
    for r in 0..25i64 {
        for a in 0..arrays.len() {
            let k = (r * 37 + a as i64) % 99 + 1;
            let answer = count_k_difference(&arrays[a], k);
            calls += 1;
            sum += answer;
            check = (check * 31 + answer) % 1000000007;
        }
    }
    println!("{} calls: sum {}, checksum {}", calls, sum, check);
}
