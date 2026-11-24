// LeetCode #1293 bench: the ★ arm over 50 grids of 40 by 40 with obstacles 30
// in 100, built once; then 80 passes, each flipping one cell of every grid and
// choosing k from the checksum so far, answering it.
use std::collections::VecDeque;

fn shortest_path(grid: &[Vec<i64>], k: i64) -> i64 {
    let m = grid.len() as i64;
    let n = grid[0].len() as i64;
    if k >= m + n - 2 {
        return m + n - 2;
    }
    let mut best = vec![vec![-1i64; n as usize]; m as usize];
    let mut queue: VecDeque<(i64, i64, i64)> = VecDeque::new();
    queue.push_back((0, 0, k));
    best[0][0] = k;
    let mut steps = 0;
    while !queue.is_empty() {
        for _ in 0..queue.len() {
            let (r, c, left) = queue.pop_front().unwrap();
            if r == m - 1 && c == n - 1 {
                return steps;
            }
            for &(dr, dc) in [(1, 0), (-1, 0), (0, 1), (0, -1)].iter() {
                let nr = r + dr;
                let nc = c + dc;
                if nr < 0 || nr >= m || nc < 0 || nc >= n {
                    continue;
                }
                let rest = left - grid[nr as usize][nc as usize];
                if rest > best[nr as usize][nc as usize] {
                    best[nr as usize][nc as usize] = rest;
                    queue.push_back((nr, nc, rest));
                }
            }
        }
        steps += 1;
    }
    -1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1293;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..50 {
        let mut grid = Vec::new();
        for i in 0..40 {
            let mut row = Vec::new();
            for j in 0..40 {
                let corner = (i == 0 && j == 0) || (i == 39 && j == 39);
                row.push(if !corner && next_random(&mut seed) % 100 < 30 { 1 } else { 0 });
            }
            grid.push(row);
        }
        grids.push(grid);
    }
    let mut check: i64 = 0;
    for p in 0..80 {
        for a in 0..grids.len() {
            let cell = (1 + check % 1598) as usize;
            grids[a][cell / 40][cell % 40] = 1 - grids[a][cell / 40][cell % 40];
            check = (check * 31 + shortest_path(&grids[a], check % 78) + 2 + p) % 1000000007;
        }
    }
    println!("80 passes over 50 grids of 40 by 40: checksum {}", check);
}
