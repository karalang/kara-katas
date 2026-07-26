// Equal-HASH Rust twin for LeetCode #128 — README caveat lane, not part of the
// results.json feed.
//
// longest_consecutive.rs uses Rust's default HashSet hasher (SipHash-1-3, which
// is DoS-resistant). Kara's Set hashes an integer with a single Fibonacci
// multiply and is NOT DoS-resistant. This kata is Set-dominated — one insert
// and at least one `contains` per element — so comparing the two directly is a
// safety mismatch on the hashing axis, exactly as on #387 and #347.
//
// This variant swaps in the same Fibonacci multiply kara uses
// (runtime/src/map.rs: `(v as u64).wrapping_mul(0x9E37_79B9_7F4A_7C15)`) so the
// Rust/kara comparison is hash-for-hash honest. See ../README.md § Benchmarks.

use std::collections::HashSet;
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

type FibSet = HashSet<i64, BuildHasherDefault<FibHasher>>;

fn longest_consecutive(nums: &[i64]) -> i64 {
    let mut s: FibSet = FibSet::default();
    for &v in nums {
        s.insert(v);
    }
    let mut best: i64 = 0;
    for &v in nums {
        if !s.contains(&(v - 1)) {
            let mut length: i64 = 1;
            let mut cur = v;
            while s.contains(&(cur + 1)) {
                cur += 1;
                length += 1;
            }
            if length > best {
                best = length;
            }
        }
    }
    best
}

fn lcg(seed: i64, n: i64, cap: i64) -> Vec<i64> {
    let mut out: Vec<i64> = Vec::new();
    let mut x = seed;
    for _ in 0..n {
        x = (x * 1103515245 + 12345) % 2147483648;
        out.push(x % cap);
    }
    out
}

fn main() {
    let np: i64 = 8;
    let n: i64 = 20000;
    let cap: i64 = 25000;
    let iters: i64 = 150;

    let arrays: Vec<Vec<i64>> = (0..np).map(|j| lcg(j + 1, n, cap)).collect();

    let mut sink: i64 = 0;
    for it in 0..iters {
        let idx = ((it * 3) % np) as usize;
        sink += longest_consecutive(&arrays[idx]);
    }
    println!("{}", sink);
}
