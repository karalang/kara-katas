// LeetCode #1046: Last Stone Weight -- benchmark driver, Rust mirror of
// last_stone.kara. std's BinaryHeap is largest-first, as the ★ arm's queue.
use std::collections::BinaryHeap;

fn last_stone_weight(stones: &[i64]) -> i64 {
    let mut heap = BinaryHeap::from(stones.to_vec());
    loop {
        let y = match heap.pop() {
            Some(y) => y,
            None => return 0,
        };
        let x = match heap.pop() {
            Some(x) => x,
            None => return y,
        };
        if y > x {
            heap.push(y - x);
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let (count, n, rounds) = (1000, 3000, 3);
    let mut seed = 1046;
    let mut piles: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut pile = Vec::new();
        for _ in 0..n {
            let high = next_random(&mut seed);
            let low = next_random(&mut seed);
            pile.push((high * 32768 + low) % 1000000000 + 1);
        }
        piles.push(pile);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        for pile in &piles {
            let answer = last_stone_weight(pile);
            total += answer;
            check = (check * 131 + answer % 1000000007 + 1) % 1000000007;
        }
    }
    println!("{} piles of {} stones, {} rounds: total {}, checksum {}", count, n, rounds, total, check);
}
