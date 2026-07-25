// Benchmark harness for LeetCode #347 — scalar-keyed Map approach.
// Mirrors top_k_frequent.kara algorithm-for-algorithm.

use std::collections::HashMap;

fn top_k_frequent(nums: &[i64], k: i64) -> Vec<i64> {
    let mut counts: HashMap<i64, i64> = HashMap::new();
    for &v in nums {
        let n = *counts.get(&v).unwrap_or(&0);
        counts.insert(v, n + 1);
    }

    let mut vals: Vec<i64> = Vec::new();
    for &v in counts.keys() {
        vals.push(v);
    }

    let mut a: usize = 1;
    while a < vals.len() {
        let cur = vals[a];
        let cur_c = *counts.get(&cur).unwrap_or(&0);
        let mut b: i64 = a as i64 - 1;
        while b >= 0 {
            let prev = vals[b as usize];
            let prev_c = *counts.get(&prev).unwrap_or(&0);
            let mut shift = false;
            if prev_c < cur_c {
                shift = true;
            }
            if prev_c == cur_c && prev > cur {
                shift = true;
            }
            if !shift {
                break;
            }
            vals[(b + 1) as usize] = prev;
            b -= 1;
        }
        vals[(b + 1) as usize] = cur;
        a += 1;
    }

    let mut limit = k as usize;
    if vals.len() < limit {
        limit = vals.len();
    }
    let mut out: Vec<i64> = Vec::new();
    for t in 0..limit {
        out.push(vals[t]);
    }
    out
}

fn main() {
    let n: i64 = 8000;
    let d: i64 = 200;
    let iters: i64 = 300;
    let k: i64 = 10;

    let mut bs: Vec<i64> = Vec::new();
    for i in 0..n {
        let mut v = i % d;
        if i % 5 == 0 {
            v = i % 13;
        }
        bs.push(v);
    }

    let mut sink: i64 = 0;
    for it in 0..iters {
        let p = ((it * 7919) % n) as usize;
        bs[p] = (it * 37) % d;
        let got = top_k_frequent(&bs, k);
        for v in got {
            sink += v;
        }
    }
    println!("{}", sink);
}
