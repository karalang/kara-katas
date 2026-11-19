// LeetCode #1631: Path With Minimum Effort -- the bench's Rust mirror: the
// ★ arm on 200 random grids of 100 x 100 heights up to 10^6, all drawn
// first. Rust's heap is largest-first, so entries go in as `Reverse`.

use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn minimum_effort_path(heights: &[Vec<i32>]) -> i32 {
    let (rows, cols) = (heights.len() as i64, heights[0].len() as i64);
    let mut best = vec![vec![i32::MAX; cols as usize]; rows as usize];
    let mut queue: BinaryHeap<Reverse<(i32, i64, i64)>> = BinaryHeap::new();
    best[0][0] = 0;
    queue.push(Reverse((0, 0, 0)));
    while let Some(Reverse((effort, r, c))) = queue.pop() {
        if r == rows - 1 && c == cols - 1 {
            return effort;
        }
        if effort > best[r as usize][c as usize] {
            continue;
        }
        for (dr, dc) in [(-1, 0), (1, 0), (0, -1), (0, 1)] {
            let (nr, nc) = (r + dr, c + dc);
            if nr < 0 || nr >= rows || nc < 0 || nc >= cols {
                continue;
            }
            let (nu, nv) = (nr as usize, nc as usize);
            let step = effort.max((heights[nu][nv] - heights[r as usize][c as usize]).abs());
            if step < best[nu][nv] {
                best[nu][nv] = step;
                queue.push(Reverse((step, nr, nc)));
            }
        }
    }
    0
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1631;
    let mut grids: Vec<Vec<Vec<i32>>> = Vec::new();
    for _ in 0..200 {
        let mut heights = Vec::new();
        for _ in 0..100 {
            let mut row = Vec::new();
            for _ in 0..100 {
                let high = next_random(&mut seed);
                row.push(((high * 32768 + next_random(&mut seed)) % 1000000 + 1) as i32);
            }
            heights.push(row);
        }
        grids.push(heights);
    }
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for heights in &grids {
        let effort = minimum_effort_path(heights) as i64;
        total += effort;
        check = (check * 31 + effort + 1) % 1000000007;
    }
    println!("200 grids of 100 x 100: efforts sum to {}, checksum {}", total, check);
}
