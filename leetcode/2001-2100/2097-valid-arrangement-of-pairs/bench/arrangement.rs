// LeetCode #2097: Valid Arrangement of Pairs -- Rust mirror of the ★ arm's
// benchmark (arrangement.kara): the same 100 random walks of 100000 pairs,
// no pair twice, each arranged by Hierholzer's walk on an explicit stack, with std's
// `HashMap` (SipHash, as Kāra's `Map`).
use std::collections::{HashMap, HashSet};

fn valid_arrangement(pairs: &[(i64, i64)]) -> Vec<(i64, i64)> {
    let mut next: HashMap<i64, Vec<i64>> = HashMap::new();
    let mut balance: HashMap<i64, i64> = HashMap::new();
    for &(a, b) in pairs {
        next.entry(a).or_default().push(b);
        next.entry(b).or_default();
        *balance.entry(a).or_insert(0) += 1;
        *balance.entry(b).or_insert(0) -= 1;
    }
    let mut start = pairs[0].0;
    for (&v, &d) in &balance {
        if d == 1 {
            start = v;
        }
    }
    let mut stack = vec![start];
    let mut path: Vec<i64> = Vec::new();
    while !stack.is_empty() {
        let top = stack[stack.len() - 1];
        match next.get_mut(&top).unwrap().pop() {
            Some(v) => stack.push(v),
            None => {
                path.push(top);
                stack.pop();
            }
        }
    }
    path.reverse();
    (1..path.len()).map(|i| (path[i - 1], path[i])).collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    hi * 32768 + next_random(seed)
}

fn step(at: i64, values: &[i64], used: &HashSet<(i64, i64)>, seed: &mut i64) -> Option<i64> {
    let k = values.len();
    let from = (next_random(seed) % k as i64) as usize;
    for j in 0..k {
        let v = values[(from + j) % k];
        if v != at && !used.contains(&(at, v)) {
            return Some(v);
        }
    }
    None
}

fn random_pairs(m: usize, k: i64, closed: bool, seed: &mut i64) -> Vec<(i64, i64)> {
    let values: Vec<i64> = (0..k).map(|_| wide_random(seed) % 1000000001).collect();
    let first = values[(next_random(seed) % k) as usize];
    let mut walk = vec![first];
    let mut used: HashSet<(i64, i64)> = HashSet::new();
    let mut at = first;
    while walk.len() <= m + 50 {
        if closed && walk.len() >= m && at != first && !used.contains(&(at, first)) {
            walk.push(first);
            break;
        }
        if !closed && walk.len() > m {
            break;
        }
        match step(at, &values, &used, seed) {
            Some(v) => {
                used.insert((at, v));
                walk.push(v);
                at = v;
            }
            None => break,
        }
    }
    let mut pairs: Vec<(i64, i64)> = (1..walk.len()).map(|i| (walk[i - 1], walk[i])).collect();
    for i in (1..pairs.len()).rev() {
        let j = (wide_random(seed) % (i as i64 + 1)) as usize;
        pairs.swap(i, j);
    }
    pairs
}

fn main() {
    let mut seed = 2097;
    let mut total = 0;
    let mut check: i64 = 0;
    for round in 0..100 {
        let pairs = random_pairs(100000, 1000, round % 2 == 0, &mut seed);
        let got = valid_arrangement(&pairs);
        total += got.len();
        for &(a, _) in &got {
            check = (check * 31 + a) % 1000000007;
        }
        check = (check * 31 + got[got.len() - 1].1) % 1000000007;
    }
    println!("100 rounds: {total} pairs, checksum {check}");
}
