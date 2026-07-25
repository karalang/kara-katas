// Equal-HASH Rust twin for LeetCode #387 — README caveat lane, not part of the
// results.json feed.
//
// first_unique_char.rs uses Rust's default HashMap hasher (SipHash-1-3, which
// is DoS-resistant). Kara's map and the hand-rolled C map both hash an integer
// key with a single Fibonacci multiply and are NOT DoS-resistant. Comparing
// those directly is a safety mismatch on the hashing axis, exactly like
// comparing `rustc -O`'s silent wrapping against kara's checked arithmetic.
//
// This variant swaps in the same Fibonacci multiply kara uses
// (runtime/src/map.rs: `(v as u64).wrapping_mul(0x9E37_79B9_7F4A_7C15)`) so the
// Rust/kara comparison is hash-for-hash honest. See ../README.md § Benchmarks.

use std::collections::HashMap;
use std::hash::{BuildHasherDefault, Hasher};

#[derive(Default)]
struct FibHasher(u64);

impl Hasher for FibHasher {
    fn finish(&self) -> u64 {
        self.0
    }
    fn write(&mut self, bytes: &[u8]) {
        for &b in bytes {
            self.0 = (self.0 ^ b as u64).wrapping_mul(0x9E37_79B9_7F4A_7C15);
        }
    }
    fn write_i64(&mut self, i: i64) {
        self.0 = (i as u64).wrapping_mul(0x9E37_79B9_7F4A_7C15);
    }
}

type FibMap = HashMap<i64, i64, BuildHasherDefault<FibHasher>>;

fn first_uniq_char(bs: &[i64]) -> i64 {
    let mut counts: FibMap = FibMap::default();
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
    let mut counts: FibMap = FibMap::default();
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
