// LeetCode #1199 bench: the ★ arm in Rust, over the same 200 sets of 1000
// blocks and 50 rounds as the Kāra bench; the smallest-first queue is a
// `BinaryHeap` of `Reverse`d times.

use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn min_build_time(blocks: Vec<i64>, split: i64) -> i64 {
    let mut queue: BinaryHeap<Reverse<i64>> = blocks.into_iter().map(Reverse).collect();
    while queue.len() > 1 {
        queue.pop();
        let Reverse(slower) = queue.pop().unwrap();
        queue.push(Reverse(slower + split));
    }
    queue.pop().unwrap().0
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let highs = [10, 1000, 100000];
    let mut seed = 1199;
    let mut sets: Vec<(Vec<i64>, i64)> = Vec::new();
    for k in 0..200 {
        let high = highs[k % 3];
        let split = next_random(&mut seed) % 100 + 1;
        let blocks: Vec<i64> = (0..1000)
            .map(|_| {
                let a = next_random(&mut seed);
                let b = next_random(&mut seed);
                (a * 32768 + b) % high + 1
            })
            .collect();
        sets.push((blocks, split));
    }
    let mut check: i64 = 0;
    for _ in 0..50 {
        for (blocks, split) in &sets {
            let t = min_build_time(blocks.clone(), *split);
            check = (check * 131 + t) % 1000000007;
        }
    }
    println!("50 rounds of 200 sets of 1000 blocks: checksum {}", check);
}
