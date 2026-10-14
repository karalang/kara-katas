// Benchmark for #560: Rust mirror of the ★ arm (prefix sums in a
// HashMap); see subarray_sum.kara. std's HashMap hashes with SipHash-1-3
// under a random key, as Kāra's Map does.
use std::collections::HashMap;

fn subarray_sum(nums: &[i64], k: i64) -> i64 {
    let mut seen: HashMap<i64, i64> = HashMap::new();
    seen.insert(0, 1);
    let mut sum = 0;
    let mut count = 0;
    for &x in nums {
        sum += x;
        count += seen.get(&(sum - k)).copied().unwrap_or(0);
        *seen.entry(sum).or_insert(0) += 1;
    }
    count
}

// ---- benchmark --------------------------------------------------------------

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 100;
    let n = 20000;
    let rounds = 20;
    let mut seed: i64 = 560;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..n {
            nums.push(step(&mut seed) % 2001 - 1000);
        }
        arrays.push(nums);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for g in 0..count {
            let k = step(&mut seed) % 2001 - 1000;
            let c = subarray_sum(&arrays[(round * 7 + g) % count], k);
            total += c;
            checksum = (checksum * 31 + c) % 1000000007;
        }
    }
    println!("{} arrays of {}, {} rounds: {} subarrays, checksum {}", count, n, rounds, total, checksum);
}
