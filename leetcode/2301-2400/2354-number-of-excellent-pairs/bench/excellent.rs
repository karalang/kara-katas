// LeetCode #2354: Number of Excellent Pairs -- the bench, the ★ arm in
// Rust: the distinct values tallied by their count of set bits, then every
// two tallies whose bits reach k multiplied.

use std::collections::HashSet;

fn count_excellent_pairs(nums: &[i64], k: i64) -> i64 {
    let distinct: HashSet<i64> = nums.iter().copied().collect();
    let mut by_bits = [0i64; 31];
    for x in &distinct {
        by_bits[x.count_ones() as usize] += 1;
    }
    let mut total = 0i64;
    for a in 0..31 {
        for b in 0..31 {
            if (a + b) as i64 >= k {
                total += by_bits[a] * by_bits[b];
            }
        }
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // array a holds 10^5 values from 1 to 10^9, from 1 to 10^(4 + a / 2)
    // distinct; pass p asks for k = 1 + (7 p + a) mod 60
    let mut seed = 2354i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    let mut spread = 10000i64;
    for a in 0..10 {
        let mut nums = Vec::new();
        for _ in 0..100000 {
            let high = next_random(&mut seed);
            nums.push(1 + (high * 32768 + next_random(&mut seed)) % spread * 99991 % 1000000000);
        }
        arrays.push(nums);
        if a % 2 == 1 {
            spread *= 10;
        }
    }
    let mut check = 0i64;
    for p in 0..20i64 {
        for a in 0..10i64 {
            let k = 1 + (7 * p + a) % 60;
            check = (check * 31 + count_excellent_pairs(&arrays[a as usize], k) + p) % 1000000007;
        }
    }
    println!("20 passes over 10 arrays of 10^5 values: checksum {}", check);
}
