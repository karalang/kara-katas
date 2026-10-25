// Benchmark: LeetCode #994 Rotting Oranges -- the ★ arm, a
// breadth-first search from every rotten orange at once, on random grids
// of 10 by 10, LeetCode's largest. Mirrors oranges_rotting.kara, .c, .py
// and go-seq/.
use std::collections::VecDeque;

fn oranges_rotting(grid: &[Vec<i64>]) -> i64 {
    let m = grid.len() as i64;
    let n = grid[0].len() as i64;
    let mut g = grid.to_vec();
    let mut queue: VecDeque<(i64, i64, i64)> = VecDeque::new();
    let mut fresh = 0;
    for r in 0..m {
        for c in 0..n {
            if g[r as usize][c as usize] == 2 {
                queue.push_back((r, c, 0));
            } else if g[r as usize][c as usize] == 1 {
                fresh += 1;
            }
        }
    }
    let steps = [(1, 0), (-1, 0), (0, 1), (0, -1)];
    let mut minutes = 0;
    while let Some((r, c, t)) = queue.pop_front() {
        minutes = t;
        for (dr, dc) in steps.iter() {
            let nr = r + dr;
            let nc = c + dc;
            if nr >= 0 && nr < m && nc >= 0 && nc < n && g[nr as usize][nc as usize] == 1 {
                g[nr as usize][nc as usize] = 2;
                fresh -= 1;
                queue.push_back((nr, nc, t + 1));
            }
        }
    }
    if fresh > 0 {
        -1
    } else {
        minutes
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_grid(seed: &mut i64) -> Vec<Vec<i64>> {
    let mut grid = Vec::new();
    for _ in 0..10 {
        let mut row = Vec::new();
        for _ in 0..10 {
            let k = next_random(seed) % 32;
            row.push(if k < 3 {
                0
            } else if k == 3 {
                2
            } else {
                1
            });
        }
        grid.push(row);
    }
    grid
}

fn main() {
    let rounds = 20000;
    let mut seed = 994;
    let grids: Vec<Vec<Vec<i64>>> = (0..20).map(|_| random_grid(&mut seed)).collect();
    let mut stuck: i64 = 0;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..20 {
            let got = oranges_rotting(&grids[(r + i) % 20]);
            if got < 0 {
                stuck += 1;
            } else {
                total += got;
            }
            check = (check * 31 + got + 2) % 1000000007;
        }
    }
    println!("{rounds} rounds over 20 grids of 10 by 10: {stuck} never rot, {total} minutes, checksum {check}");
}
