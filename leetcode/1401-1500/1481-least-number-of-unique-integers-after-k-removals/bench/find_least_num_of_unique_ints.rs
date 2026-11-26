// LeetCode #1481: Least Number of Unique Integers after K Removals --
// bench, Rust mirror of find_least_num_of_unique_ints.kara (std's
// `HashMap`, SipHash-1-3 under a random key, as Kāra's `Map` is)
use std::collections::HashMap;

fn find_least_num_of_unique_ints(arr: &[i32], k: i32) -> i32 {
    let mut count: HashMap<i32, i64> = HashMap::new();
    for &x in arr.iter() {
        *count.entry(x).or_insert(0) += 1;
    }
    let mut counts: Vec<i64> = count.values().copied().collect();
    counts.sort();
    let mut left: i64 = k as i64;
    let mut unique = counts.len() as i64;
    for &c in counts.iter() {
        if c > left {
            break;
        }
        left -= c;
        unique -= 1;
    }
    unique as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1481;
    let mut arr: Vec<i32> = (0..100000).map(|_| (1 + next_random(&mut seed) % 30000) as i32).collect();
    let mut check: i64 = 0;
    for pass in 0..100i64 {
        arr[(check % 100000) as usize] = (1 + (check / 7) % 30000) as i32;
        let k = (check % 100000) as i32;
        check = (check * 31 + find_least_num_of_unique_ints(&arr, k) as i64 + pass) % 1000000007;
    }
    println!("100 passes over 100000 values: checksum {}", check);
}
