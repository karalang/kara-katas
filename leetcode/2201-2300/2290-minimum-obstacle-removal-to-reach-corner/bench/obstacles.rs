// LeetCode #2290: Minimum Obstacle Removal to Reach Corner -- the bench,
// the ★ arm in Rust. A 0-1 breadth-first search over a `VecDeque`: a
// step onto an empty cell to the front, one onto an obstacle to the back.

use std::collections::VecDeque;

fn minimum_obstacles(grid: &[Vec<i64>]) -> i64 {
    let m = grid.len() as i64;
    let n = grid[0].len() as i64;
    let mut cost = vec![-1i64; (m * n) as usize];
    let mut best = vec![i64::MAX; (m * n) as usize];
    let mut queue: VecDeque<(i64, i64)> = VecDeque::new();
    best[0] = 0;
    queue.push_back((0, 0));
    let moves = [(0, 1), (1, 0), (0, -1), (-1, 0)];
    while let Some((r, c)) = queue.pop_front() {
        if cost[(r * n + c) as usize] >= 0 {
            continue;
        }
        let here = best[(r * n + c) as usize];
        cost[(r * n + c) as usize] = here;
        if r == m - 1 && c == n - 1 {
            return here;
        }
        for &(dr, dc) in moves.iter() {
            let (nr, nc) = (r + dr, c + dc);
            if nr < 0 || nc < 0 || nr >= m || nc >= n {
                continue;
            }
            let step = grid[nr as usize][nc as usize];
            let to = (nr * n + nc) as usize;
            if here + step < best[to] {
                best[to] = here + step;
                if step == 0 {
                    queue.push_front((nr, nc));
                } else {
                    queue.push_back((nr, nc));
                }
            }
        }
    }
    best[(m * n - 1) as usize]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2290;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..10 {
        let mut grid: Vec<Vec<i64>> = Vec::new();
        for _ in 0..200 {
            let row: Vec<i64> = (0..200).map(|_| if next_random(&mut seed) % 10 < 4 { 1 } else { 0 }).collect();
            grid.push(row);
        }
        grid[0][0] = 0;
        grid[199][199] = 0;
        grids.push(grid);
    }
    let mut check: i64 = 0;
    for _ in 0..5 {
        let mut total = 0;
        for grid in &grids {
            total += minimum_obstacles(grid);
        }
        check = (check * 31 + total) % 1000000007;
    }
    println!("5 passes over 10 grids of 200x200: checksum {}", check);
}
