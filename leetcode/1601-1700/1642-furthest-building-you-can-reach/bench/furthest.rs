// LeetCode #1642: Furthest Building You Can Reach -- the bench's Rust
// mirror: the ★ arm on 50 random rows of 100000 buildings up to 10^4 high,
// each with up to 10^9 bricks and up to 5000 ladders, all drawn first.

use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn furthest_building(heights: &Vec<i32>, bricks: i32, ladders: i32) -> i64 {
    let mut laddered: BinaryHeap<Reverse<i32>> = BinaryHeap::new();
    let mut bricks = bricks;
    for i in 1..heights.len() {
        let climb = heights[i] - heights[i - 1];
        if climb <= 0 {
            continue;
        }
        laddered.push(Reverse(climb));
        if laddered.len() > ladders as usize {
            bricks -= laddered.pop().unwrap().0;
            if bricks < 0 {
                return i as i64 - 1;
            }
        }
    }
    heights.len() as i64 - 1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1642;
    let mut rows = Vec::new();
    for _ in 0..50 {
        let mut heights = Vec::new();
        for _ in 0..100000 {
            heights.push((next_random(&mut seed) % 10000 + 1) as i32);
        }
        let bricks = ((next_random(&mut seed) * 32768 + next_random(&mut seed)) % 1000000001) as i32;
        let ladders = (next_random(&mut seed) % 5001) as i32;
        rows.push((heights, bricks, ladders));
    }
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for (heights, bricks, ladders) in &rows {
        let furthest = furthest_building(heights, *bricks, *ladders);
        total += furthest;
        check = (check * 31 + furthest + 1) % 1000000007;
    }
    println!("50 rows of 100000 buildings: indices sum to {}, checksum {}", total, check);
}
