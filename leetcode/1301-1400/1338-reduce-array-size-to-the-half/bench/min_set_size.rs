// LeetCode #1338 bench, Rust mirror of the Kāra bench: the ★ arm on 20
// arrays of 10^5 values built once, then 30 passes, each setting one value
// of every array from the checksum so far, answering every array.

use std::collections::HashMap;

fn min_set_size(arr: &[i32]) -> i32 {
    let mut counts: HashMap<i32, i64> = HashMap::new();
    for &x in arr.iter() {
        *counts.entry(x).or_insert(0) += 1;
    }
    let mut sizes: Vec<i64> = counts.values().cloned().collect();
    sizes.sort_by(|a, b| b.cmp(a));
    let mut removed = 0i64;
    let mut chosen = 0;
    for &s in sizes.iter() {
        if 2 * removed >= arr.len() as i64 {
            break;
        }
        removed += s;
        chosen += 1;
    }
    chosen
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n = 100000i64;
    let mut seed = 1338i64;
    let mut arrays: Vec<Vec<i32>> = Vec::new();
    for t in 0..20 {
        let top = if t % 2 == 0 { 100000 } else { 1000 };
        let mut arr: Vec<i32> = Vec::new();
        for _ in 0..n {
            let a = next_random(&mut seed);
            arr.push((1 + (a * 32768 + next_random(&mut seed)) % top) as i32);
        }
        arrays.push(arr);
    }
    let mut check: i64 = 0;
    for pass in 0..30i64 {
        for t in 0..20 {
            let at = (check % n) as usize;
            arrays[t][at] = (1 + check / 3 % 1000) as i32;
            let answer = min_set_size(&arrays[t]);
            check = (check * 31 + answer as i64 + pass) % 1000000007;
        }
    }
    println!("30 passes over 20 arrays of 10^5: checksum {}", check);
}
