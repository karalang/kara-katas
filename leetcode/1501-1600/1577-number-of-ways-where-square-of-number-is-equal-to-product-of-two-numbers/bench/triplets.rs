// LeetCode #1577: Number of Ways Where Square of Number Is Equal to
// Product of Two Numbers -- bench: the ★ arm (a walk with a Map of the
// values seen) over 10 pairs of arrays of 1000 values, each a power of 2
// or 3 times a factor below 100, drawn first.

use std::collections::HashMap;

fn ways(squares: &[i64], products: &[i64]) -> i64 {
    let mut total = 0;
    for &x in squares {
        let target = x * x;
        let mut seen: HashMap<i64, i64> = HashMap::new();
        for &y in products {
            if target % y == 0 {
                total += seen.get(&(target / y)).copied().unwrap_or(0);
            }
            *seen.entry(y).or_insert(0) += 1;
        }
    }
    total
}

fn num_triplets(nums1: &[i64], nums2: &[i64]) -> i64 {
    ways(nums1, nums2) + ways(nums2, nums1)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1577;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let nums: Vec<i64> = (0..1000)
            .map(|_| {
                let mut v = next_random(&mut seed) % 100 + 1;
                for _ in 0..next_random(&mut seed) % 4 {
                    v *= 2 + next_random(&mut seed) % 2;
                }
                v.min(100000)
            })
            .collect();
        arrays.push(nums);
    }
    let (mut check, mut total) = (0i64, 0i64);
    for p in 0..10 {
        let w = num_triplets(&arrays[2 * p], &arrays[2 * p + 1]);
        total += w;
        check = mix(check, w);
    }
    println!("10 pairs of arrays of 1000 values: triplets total {}, checksum {}", total, check);
}
