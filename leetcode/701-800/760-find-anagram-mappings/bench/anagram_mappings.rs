// LeetCode 760 — Find Anagram Mappings: benchmark, the ★ arm in Rust.
use std::collections::HashMap;

fn anagram_mappings(nums1: &[i64], nums2: &[i64]) -> Vec<i64> {
    let mut positions: HashMap<i64, Vec<i64>> = HashMap::new();
    for (j, x) in nums2.iter().enumerate() {
        positions.entry(*x).or_default().push(j as i64);
    }
    let mut used: HashMap<i64, usize> = HashMap::new();
    let mut mapping: Vec<i64> = Vec::new();
    for x in nums1 {
        let k = *used.get(x).unwrap_or(&0);
        mapping.push(positions[x][k]);
        used.insert(*x, k + 1);
    }
    mapping
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 100000;
    let mut seed = 760;
    let mut fixed = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        let mut nums1: Vec<i64> = Vec::new();
        for _ in 0..100 {
            nums1.push(next_random(&mut seed) % 50);
        }
        let mut nums2 = nums1.clone();
        for i in 0..100 {
            let j = i + (next_random(&mut seed) % (100 - i as i64)) as usize;
            nums2.swap(i, j);
        }
        let mapping = anagram_mappings(&nums1, &nums2);
        for i in 0..100 {
            if mapping[i] == i as i64 {
                fixed += 1;
            }
            check = (check * 31 + mapping[i]) % 1000000007;
        }
    }
    println!("{rounds} pairs of 100 values: {fixed} mapped to their own index, checksum {check}");
}
