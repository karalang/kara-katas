// The Rust mirror of count_triplets.kara: a fresh HashMap for every array,
// as the Kara arm makes a fresh Map, both hashing with SipHash.
use std::collections::HashMap;

fn count_triplets(arr: &[i32]) -> i32 {
    let mut seen: HashMap<i32, (i64, i64)> = HashMap::new();
    seen.insert(0, (1, 0));
    let mut x: i32 = 0;
    let mut count: i64 = 0;
    for (k, &a) in arr.iter().enumerate() {
        x ^= a;
        let (times, places) = seen.get(&x).copied().unwrap_or((0, 0));
        count += times * k as i64 - places;
        seen.insert(x, (times + 1, places + k as i64 + 1));
    }
    count as i32
}

fn main() {
    let mut seed: i64 = 1442;
    let mut arrays: Vec<Vec<i32>> = Vec::new();
    for _ in 0..2000 {
        let mut arr: Vec<i32> = Vec::new();
        for _ in 0..300 {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            arr.push((1 + seed / 65536 % 1023) as i32);
        }
        arrays.push(arr);
    }
    let mut check: i64 = 0;
    for _ in 0..50 {
        for arr in arrays.iter() {
            check = (check * 131 + count_triplets(arr) as i64) % 1000000007;
        }
    }
    println!("10^5 arrays of 300: checksum {}", check);
}
