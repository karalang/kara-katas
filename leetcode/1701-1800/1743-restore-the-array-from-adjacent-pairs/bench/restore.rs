// LeetCode #1743: Restore the Array From Adjacent Pairs -- the bench
// (restore.kara in Rust): the pairs as a graph, walked from an end.

use std::collections::{HashMap, HashSet};

fn restore_array(adjacent_pairs: &[Vec<i32>]) -> Vec<i32> {
    let mut next: HashMap<i32, Vec<i32>> = HashMap::new();
    for pair in adjacent_pairs.iter() {
        next.entry(pair[0]).or_insert_with(Vec::new).push(pair[1]);
        next.entry(pair[1]).or_insert_with(Vec::new).push(pair[0]);
    }
    let start = *next.iter().find(|(_, near)| near.len() == 1).unwrap().0;
    let mut order: Vec<i32> = vec![start, next[&start][0]];
    while order.len() < adjacent_pairs.len() + 1 {
        let (before, last) = (order[order.len() - 2], order[order.len() - 1]);
        let near = &next[&last];
        order.push(if near[0] == before { near[1] } else { near[0] });
    }
    order
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    next_random(seed) * 32768 + next_random(seed)
}

fn random_pairs(n: usize, seed: &mut i64) -> Vec<Vec<i32>> {
    let mut taken: HashSet<i64> = HashSet::new();
    let mut values: Vec<i32> = Vec::new();
    while values.len() < n {
        let v = wide(seed) % 200001 - 100000;
        if taken.insert(v) {
            values.push(v as i32);
        }
    }
    let mut pairs: Vec<Vec<i32>> = Vec::new();
    for i in 1..n {
        if next_random(seed) % 2 == 0 {
            pairs.push(vec![values[i - 1], values[i]]);
        } else {
            pairs.push(vec![values[i], values[i - 1]]);
        }
    }
    for i in (1..pairs.len()).rev() {
        let j = ((next_random(seed) * 32768 + next_random(seed)) % (i as i64 + 1)) as usize;
        pairs.swap(i, j);
    }
    pairs
}

fn main() {
    let count = 10;
    let rounds: i64 = 4;
    let n = 100000;
    let mut seed: i64 = 1743;
    let problems: Vec<Vec<Vec<i32>>> = (0..count).map(|_| random_pairs(n, &mut seed)).collect();
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for pairs in problems.iter() {
            let order = restore_array(pairs);
            let (first, last) = (order[0], order[order.len() - 1]);
            let middle = if first < last { order[order.len() / 2] } else { order[order.len() - 1 - order.len() / 2] };
            let low = first.min(last) as i64;
            sum += low;
            check = (check * 31 + low + middle as i64 + 200000 + r) % 1000000007;
        }
    }
    println!("{} arrays of {} values, {} rounds: smaller ends sum to {}, checksum {}", count, n, rounds, sum, check);
}
