// LeetCode #2406: Divide Intervals Into Minimum Number of Groups -- the
// bench, the ★ arm in Rust: the intervals sorted by left end, and a
// `BinaryHeap` of `Reverse` right ends, the smallest first.

use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn min_groups(intervals: &[(i64, i64)]) -> i64 {
    let mut order = intervals.to_vec();
    order.sort();
    let mut ends: BinaryHeap<Reverse<i64>> = BinaryHeap::new();
    for &(left, right) in &order {
        if let Some(&Reverse(e)) = ends.peek() {
            if e < left {
                ends.pop();
            }
        }
        ends.push(Reverse(right));
    }
    ends.len() as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2406;
    let mut sets: Vec<Vec<(i64, i64)>> = Vec::new();
    for i in 0..10i64 {
        let iv: Vec<(i64, i64)> = (0..100000)
            .map(|_| {
                let left = 1 + (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 900000;
                (left, left + (next_random(&mut seed) * 32768 + next_random(&mut seed)) % (1 + 1000 * i))
            })
            .collect();
        sets.push(iv);
    }
    let mut check: i64 = 0;
    for p in 0..5 {
        for iv in &sets {
            check = (check * 31 + min_groups(iv) + p) % 1000000007;
        }
    }
    println!("5 passes over 10 sets of 10^5 intervals: checksum {}", check);
}
