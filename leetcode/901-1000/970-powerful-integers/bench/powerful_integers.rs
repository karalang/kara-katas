// Benchmark: LeetCode #970 Powerful Integers -- the ★ arm, every pair of
// powers in a set, for every x and y from 1 to 100 with bound 10^6.
// Mirrors powerful_integers.kara, .c, .py and go-seq/.

use std::collections::HashSet;

fn powers(base: i64, bound: i64) -> Vec<i64> {
    let mut out = Vec::new();
    let mut p = 1;
    while p <= bound {
        out.push(p);
        if base == 1 {
            break;
        }
        p *= base;
    }
    out
}

fn powerful_integers(x: i64, y: i64, bound: i64) -> Vec<i64> {
    let mut seen = HashSet::new();
    for a in powers(x, bound) {
        for b in powers(y, bound - a) {
            seen.insert(a + b);
        }
    }
    seen.into_iter().collect()
}

fn main() {
    let rounds = 100;
    let mut found: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for x in 1..=100 {
            for y in 1..=100 {
                for v in powerful_integers(x, y, 1000000 - r) {
                    found += 1;
                    check = (check + v * v) % 1000000007;
                }
            }
        }
    }
    println!("{rounds} rounds over x and y from 1 to 100: {found} powerful integers, checksum {check}");
}
