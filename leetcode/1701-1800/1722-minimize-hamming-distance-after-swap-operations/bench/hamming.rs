// LeetCode #1722: Minimize Hamming Distance After Swap Operations -- the
// bench (hamming.kara): the swaps joined into groups with a union-find,
// each group's source values counted, and each target value matched from
// its group's counts.

use std::collections::HashMap;

fn find(parent: &mut [usize], x: usize) -> usize {
    let mut x = x;
    while parent[x] != x {
        parent[x] = parent[parent[x]];
        x = parent[x];
    }
    x
}

fn minimum_hamming_distance(source: &[i32], target: &[i32], allowed_swaps: &[Vec<i32>]) -> i32 {
    let n = source.len();
    let mut parent: Vec<usize> = (0..n).collect();
    let mut size: Vec<i64> = vec![1; n];
    for swap in allowed_swaps {
        let mut a = find(&mut parent, swap[0] as usize);
        let mut b = find(&mut parent, swap[1] as usize);
        if a == b {
            continue;
        }
        if size[a] < size[b] {
            std::mem::swap(&mut a, &mut b);
        }
        parent[b] = a;
        size[a] += size[b];
    }
    let mut counts: HashMap<(usize, i32), i64> = HashMap::new();
    for i in 0..n {
        *counts.entry((find(&mut parent, i), source[i])).or_insert(0) += 1;
    }
    let mut distance = 0;
    for i in 0..n {
        let key = (find(&mut parent, i), target[i]);
        match counts.get_mut(&key) {
            Some(c) if *c > 0 => *c -= 1,
            _ => distance += 1,
        }
    }
    distance
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    hi * 32768 + next_random(seed)
}

fn main() {
    let count = 10;
    let rounds: i64 = 5;
    let n: i64 = 100000;
    let mut seed: i64 = 1722;
    let mut problems: Vec<(Vec<i32>, Vec<i32>, Vec<Vec<i32>>)> = Vec::new();
    for _ in 0..count {
        let source: Vec<i32> = (0..n).map(|_| (wide(&mut seed) % 100000 + 1) as i32).collect();
        let target: Vec<i32> = (0..n).map(|_| (wide(&mut seed) % 100000 + 1) as i32).collect();
        let mut allowed: Vec<Vec<i32>> = Vec::new();
        for _ in 0..n {
            let a = wide(&mut seed) % n;
            let mut b = wide(&mut seed) % (n - 1);
            if b >= a {
                b += 1;
            }
            allowed.push(vec![a as i32, b as i32]);
        }
        problems.push((source, target, allowed));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (source, target, allowed) in problems.iter() {
            let answer = minimum_hamming_distance(source, target, allowed) as i64;
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{} problems of {} values and {} swaps, {} rounds: distances sum to {}, checksum {}", count, n, n, rounds, sum, check);
}
