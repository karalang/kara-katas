// LeetCode #2363: Merge Similar Items -- the bench, the ★ arm in Rust:
// every item of both lists added into a `BTreeMap` from value to total
// weight, which walks out in order of value.

use std::collections::BTreeMap;

fn merge_similar_items(items1: &[Vec<i64>], items2: &[Vec<i64>]) -> Vec<Vec<i64>> {
    let mut totals: BTreeMap<i64, i64> = BTreeMap::new();
    for item in items1.iter().chain(items2.iter()) {
        *totals.entry(item[0]).or_insert(0) += item[1];
    }
    totals.iter().map(|(&value, &weight)| vec![value, weight]).collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_items(seed: &mut i64, count: usize) -> Vec<Vec<i64>> {
    // count distinct values from 1 to 1000 in a shuffled order, each with
    // a weight of 1 to 1000
    let mut values: Vec<i64> = (1..1001).collect();
    for i in (1..1000usize).rev() {
        let j = next_random(seed) % (i as i64 + 1);
        values.swap(i, j as usize);
    }
    (0..count).map(|i| vec![values[i], 1 + next_random(seed) % 1000]).collect()
}

fn main() {
    // pair a: lists of 100 (a + 1) and 1000 - 50 a items
    let mut seed = 2363i64;
    let mut pairs: Vec<(Vec<Vec<i64>>, Vec<Vec<i64>>)> = Vec::new();
    for a in 0..10usize {
        let items1 = random_items(&mut seed, 100 * (a + 1));
        let items2 = random_items(&mut seed, 1000 - 50 * a);
        pairs.push((items1, items2));
    }
    let mut check = 0i64;
    for p in 0..400i64 {
        for (items1, items2) in &pairs {
            let merged = merge_similar_items(items1, items2);
            let last = &merged[merged.len() - 1];
            check = (check * 31 + merged.len() as i64 * 1009 + last[1] + p) % 1000000007;
        }
    }
    println!("400 passes over 10 pairs of lists: checksum {}", check);
}
