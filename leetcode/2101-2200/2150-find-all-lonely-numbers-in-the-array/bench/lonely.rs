// LeetCode #2150: Find All Lonely Numbers in the Array -- the benchmark's
// Rust mirror of lonely.kara.

use std::collections::HashMap;

fn find_lonely(nums: &[i64]) -> Vec<i64> {
    let mut count: HashMap<i64, i64> = HashMap::new();
    for &x in nums {
        *count.entry(x).or_insert(0) += 1;
    }
    count
        .iter()
        .filter(|(&x, &c)| c == 1 && !count.contains_key(&(x - 1)) && !count.contains_key(&(x + 1)))
        .map(|(&x, _)| x)
        .collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2150;
    let n: i64 = 100000;
    let mut lists: Vec<Vec<i64>> = Vec::new();
    for _ in 0..4 {
        let nums: Vec<i64> = (0..n).map(|_| wide(&mut seed) % 1000001).collect();
        lists.push(nums);
    }
    let mut total = 0;
    let mut check = 0;
    for round in 0..25 {
        for l in 0..4 {
            let at = (wide(&mut seed) % n) as usize;
            lists[l][at] = wide(&mut seed) % 1000001;
            let out = find_lonely(&lists[l]);
            let sum: i64 = out.iter().sum();
            total += out.len() as i64;
            check = (check * 31 + sum % 1000000007 + out.len() as i64 + round) % 1000000007;
        }
    }
    println!("100 searches: {} lonely in all, checksum {}", total, check);
}
