// Benchmark harness for LeetCode #387 — Map (general-alphabet) approach.
// Mirrors first_unique_char.kara algorithm-for-algorithm.

use std::collections::HashMap;

fn first_uniq_char(bs: &[i64]) -> i64 {
    let mut counts: HashMap<i64, i64> = HashMap::new();
    for &c in bs {
        let n = *counts.get(&c).unwrap_or(&0);
        counts.insert(c, n + 1);
    }

    for (j, &c) in bs.iter().enumerate() {
        let n = *counts.get(&c).unwrap_or(&0);
        if n == 1 {
            return j as i64;
        }
    }
    -1
}

fn unique_count(bs: &[i64]) -> i64 {
    let mut counts: HashMap<i64, i64> = HashMap::new();
    for &c in bs {
        let n = *counts.get(&c).unwrap_or(&0);
        counts.insert(c, n + 1);
    }
    let mut uniq: i64 = 0;
    for k in counts.keys() {
        let n = *counts.get(k).unwrap_or(&0);
        if n == 1 {
            uniq += 1;
        }
    }
    uniq
}

fn main() {
    let n: i64 = 4000;
    let iters: i64 = 2000;

    let mut bs: Vec<i64> = Vec::new();
    for i in 0..n {
        bs.push(97 + (i % 25));
    }
    bs[(n - 1) as usize] = 122;

    let mut sink: i64 = 0;
    for it in 0..iters {
        let p = ((it * 7919) % n) as usize;
        bs[p] = 97 + (it % 25);
        sink += first_uniq_char(&bs);
        sink += unique_count(&bs);
    }
    println!("{}", sink);
}
