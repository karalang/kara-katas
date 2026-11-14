// LeetCode #1552: Magnetic Force Between Two Balls -- bench: the ★ arm (a
// binary search on the answer, a greedy check) over 20 baskets of 100000
// distinct positions up to 10^9, built once, each asked 5 times with its own
// number of balls every time. Rust mirror of magnetic.kara.

use std::collections::HashSet;

fn fits(sorted: &[i64], m: i64, gap: i64) -> bool {
    let mut placed = 1;
    let mut last = sorted[0];
    for &p in sorted {
        if p - last >= gap {
            placed += 1;
            last = p;
        }
    }
    placed >= m
}

fn max_distance(position: &[i64], m: i64) -> i64 {
    let mut sorted = position.to_vec();
    sorted.sort();
    let mut lo = 1;
    let mut hi = sorted[sorted.len() - 1] - sorted[0];
    while lo < hi {
        let mid = lo + (hi - lo + 1) / 2;
        if fits(&sorted, m, mid) {
            lo = mid;
        } else {
            hi = mid - 1;
        }
    }
    lo
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1552i64;
    let mut baskets: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let mut taken = HashSet::new();
        let mut position = Vec::new();
        while position.len() < 100000 {
            let p = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 1000000000 + 1;
            if taken.insert(p) {
                position.push(p);
            }
        }
        baskets.push(position);
    }
    let mut check = 0i64;
    for pass in 0..5i64 {
        for b in 0..baskets.len() {
            let m = (pass * 20 + b as i64) * 997 % 99999 + 2;
            check = mix(check, max_distance(&baskets[b], m));
        }
    }
    println!("5 passes over 20 baskets of 100000 positions: checksum {}", check);
}
