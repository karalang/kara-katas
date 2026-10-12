// Benchmark for #454: mirror of four_sum.kara (the ★ arm, pair sums of
// the first two arrays counted in a map) on the same workload.

use std::collections::HashMap;

fn four_sum_count(nums1: &[i64], nums2: &[i64], nums3: &[i64], nums4: &[i64]) -> i64 {
    let mut sums: HashMap<i64, i64> = HashMap::new();
    for &a in nums1 {
        for &b in nums2 {
            *sums.entry(a + b).or_insert(0) += 1;
        }
    }
    let mut count = 0;
    for &c in nums3 {
        for &d in nums4 {
            count += sums.get(&-(c + d)).copied().unwrap_or(0);
        }
    }
    count
}

// ---- benchmark --------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_value(seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    let lo = next_random(seed);
    (hi * 65536 + lo) % 100001 - 50000
}

fn main() {
    let n: i64 = 1000;
    let rounds = 10;
    let mut seed: i64 = 454;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..4 {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..n {
            nums.push(random_value(&mut seed));
        }
        arrays.push(nums);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        for a in 0..4 {
            let at = (next_random(&mut seed) % n) as usize;
            arrays[a][at] = random_value(&mut seed);
        }
        let tuples = four_sum_count(&arrays[0], &arrays[1], &arrays[2], &arrays[3]);
        total += tuples;
        checksum = (checksum * 31 + tuples) % 1000000007;
    }
    println!("{rounds} rounds on 4 arrays of {n}: {total} tuples, checksum {checksum}");
}
