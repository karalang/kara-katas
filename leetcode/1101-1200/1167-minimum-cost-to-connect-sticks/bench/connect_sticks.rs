// LeetCode #1167: Minimum Cost to Connect Sticks -- the ★ arm's bench in
// Rust: a BinaryHeap of Reverse lengths built in O(n), the two shortest
// joined and the join pushed back.

use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn connect_sticks(sticks: Vec<i64>) -> i64 {
    let mut pq: BinaryHeap<Reverse<i64>> = BinaryHeap::from(sticks.into_iter().map(Reverse).collect::<Vec<_>>());
    let mut cost = 0;
    while pq.len() > 1 {
        let Reverse(a) = pq.pop().unwrap();
        let Reverse(b) = pq.pop().unwrap();
        cost += a + b;
        pq.push(Reverse(a + b));
    }
    cost
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1167;
    let mut piles: Vec<Vec<i64>> = Vec::new();
    for _ in 0..16 {
        piles.push((0..10000).map(|_| 1 + next_random(&mut seed) % 10000).collect());
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..40 {
        for k in 0..16 {
            let at = (next_random(&mut seed) % 10000) as usize;
            piles[k][at] = 1 + next_random(&mut seed) % 10000;
            let c = connect_sticks(piles[k].clone());
            total += c;
            check = (check * 31 + c) % 1000000007;
        }
    }
    println!("40 rounds over 16 piles of 10^4 sticks: total {total}, checksum {check}");
}
