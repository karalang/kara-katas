// Benchmark: LeetCode #1102 Path With Maximum Minimum Value -- a
// best-first search with a max-heap, as the Kāra ★ arm. Mirrors
// maximum_minimum_path.kara.
use std::collections::BinaryHeap;

fn maximum_minimum_path(grid: &Vec<Vec<i64>>) -> i64 {
    let (m, n) = (grid.len() as i64, grid[0].len() as i64);
    let mut done = vec![vec![false; n as usize]; m as usize];
    let mut queue: BinaryHeap<(i64, i64, i64)> = BinaryHeap::new();
    queue.push((grid[0][0], 0, 0));
    while let Some((low, r, c)) = queue.pop() {
        if done[r as usize][c as usize] {
            continue;
        }
        done[r as usize][c as usize] = true;
        if r == m - 1 && c == n - 1 {
            return low;
        }
        for (dr, dc) in [(0, 1), (1, 0), (0, -1), (-1, 0)] {
            let (nr, nc) = (r + dr, c + dc);
            if nr >= 0 && nr < m && nc >= 0 && nc < n && !done[nr as usize][nc as usize] {
                queue.push((low.min(grid[nr as usize][nc as usize]), nr, nc));
            }
        }
    }
    -1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1102;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..32 {
        grids.push((0..100).map(|_| (0..100).map(|_| next_random(&mut seed) * 30517 % 1000000000).collect()).collect());
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for round in 0..8i64 {
        for j in 0..grids.len() {
            let at = ((round * 7919 + j as i64 * 104729) % 10000) as usize;
            let (r, c) = (at / 100, at % 100);
            grids[j][r][c] /= 2;
            let best = maximum_minimum_path(&grids[j]);
            total += best;
            check = (check * 31 + best % 1000003 + 1) % 1000000007;
        }
    }
    println!("8 rounds over 32 grids of 100 by 100: minimums total {}, checksum {}", total, check);
}
