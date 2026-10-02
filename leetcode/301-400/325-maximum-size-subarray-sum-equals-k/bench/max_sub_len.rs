// Benchmark workload for LeetCode #325 — Rust mirror of max_sub_len.kara.
//
// std `HashMap`, whose default hasher is SipHash-1-3 under a random per-map
// key: the same hash function, keyed the same way, as Kara's default `Map`.
// A fresh map per call, `get` for the lookup, `entry().or_insert()` for the
// first-occurrence insert, exactly as the Kara arm.

use std::collections::HashMap;

const LEN: i64 = 200000;
const PUNCHES: i64 = 60;
const MODULUS: i64 = 1073741789;

fn max_sub_len(nums: &[i64], k: i64) -> i64 {
    let mut first: HashMap<i64, i64> = HashMap::new();
    first.insert(0, -1);
    let mut p = 0i64;
    let mut best = 0i64;
    for i in 0..nums.len() as i64 {
        p += nums[i as usize];
        if let Some(&j) = first.get(&(p - k)) {
            if i - j > best {
                best = i - j;
            }
        }
        first.entry(p).or_insert(i);
    }
    best
}

fn next(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 325i64;
    let ranges = [1i64, 100, 10000];
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for &r in &ranges {
        let mut a = Vec::new();
        for _ in 0..LEN {
            a.push(next(&mut seed) % (2 * r + 1) - r);
        }
        arrays.push(a);
    }

    let mut sink = 0i64;
    for punch in 0..PUNCHES {
        let t = (punch % 3) as usize;
        let r = ranges[t];
        let pos = (next(&mut seed) * 32768 + next(&mut seed)) % LEN;
        arrays[t][pos as usize] = next(&mut seed) % (2 * r + 1) - r;
        let k = (next(&mut seed) % 41 - 20) * r / 4;
        let len = max_sub_len(&arrays[t], k);
        sink = (sink * 31 + len + 1) % MODULUS;
    }
    println!("sink {}", sink);
}
