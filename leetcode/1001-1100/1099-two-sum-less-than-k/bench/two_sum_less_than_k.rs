// Benchmark: LeetCode #1099 Two Sum Less Than K -- Rust mirror of
// two_sum_less_than_k.kara: the ★ arm, sorting and two pointers, over 64
// arrays of 100 values built once, 400 rounds each changing one value per
// array and asking for 8 values of k.

fn two_sum_less_than_k(nums: &[i64], k: i64) -> i64 {
    let mut v = nums.to_vec();
    v.sort();
    let mut best = -1;
    let mut lo = 0usize;
    let mut hi = v.len() - 1;
    while lo < hi {
        let sum = v[lo] + v[hi];
        if sum < k {
            best = best.max(sum);
            lo += 1;
        } else {
            hi -= 1;
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1099;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..64 {
        arrays.push((0..100).map(|_| next_random(&mut seed) % 1000 + 1).collect());
    }
    let mut found = 0i64;
    let mut check = 0i64;
    for round in 0..400i64 {
        for j in 0..arrays.len() {
            let at = ((round * 7 + j as i64 * 13) % 100) as usize;
            arrays[j][at] = (arrays[j][at] + round * 31) % 1000 + 1;
            for q in 0..8i64 {
                let k = (round * 97 + j as i64 * 61 + q * 251) % 2000 + 1;
                let best = two_sum_less_than_k(&arrays[j], k);
                if best >= 0 {
                    found += 1;
                }
                check = (check * 31 + best + 1) % 1000000007;
            }
        }
    }
    println!("400 rounds over 64 arrays of 100 values: {} of 204800 with a pair, checksum {}", found, check);
}
