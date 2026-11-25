// LeetCode #1368 bench -- Rust: a 0-1 breadth-first search over the
// cells, a step the sign points to costing 0 and going to the front of
// the deque, any other costing 1 and going to its back.
use std::collections::VecDeque;

fn min_cost(grid: &[Vec<i32>]) -> i32 {
    let (m, n) = (grid.len() as i64, grid[0].len() as i64);
    // signs 1 to 4: right, left, down, up
    let moves = [(0i64, 1i64), (0, -1), (1, 0), (-1, 0)];
    let mut cost = vec![vec![i32::MAX; n as usize]; m as usize];
    let mut deque: VecDeque<(i64, i64)> = VecDeque::new();
    cost[0][0] = 0;
    deque.push_back((0, 0));
    while let Some((r, c)) = deque.pop_front() {
        for d in 0..4 {
            let (nr, nc) = (r + moves[d].0, c + moves[d].1);
            if nr < 0 || nr >= m || nc < 0 || nc >= n {
                continue;
            }
            let step = if grid[r as usize][c as usize] == (d + 1) as i32 { 0 } else { 1 };
            let through = cost[r as usize][c as usize] + step;
            if through < cost[nr as usize][nc as usize] {
                cost[nr as usize][nc as usize] = through;
                if step == 0 {
                    deque.push_front((nr, nc));
                } else {
                    deque.push_back((nr, nc));
                }
            }
        }
    }
    cost[m as usize - 1][n as usize - 1]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 20 grids of 100 by 100 signs, the constraints' most, built once;
    // then 600 rounds, each changing one cell's sign and finding the
    // cheapest valid path through that grid, all drawn from the checksum
    // so far
    let mut seed = 1368i64;
    let mut grids: Vec<Vec<Vec<i32>>> = Vec::new();
    for _ in 0..20 {
        let mut grid = Vec::new();
        for _ in 0..100 {
            let row: Vec<i32> = (0..100).map(|_| (1 + next_random(&mut seed) % 4) as i32).collect();
            grid.push(row);
        }
        grids.push(grid);
    }
    let mut check: i64 = 0;
    for r in 0..600i64 {
        let g = (check % 20) as usize;
        let cell = ((check / 20) % 10000) as usize;
        grids[g][cell / 100][cell % 100] = (1 + (check / 200000) % 4) as i32;
        let cost = min_cost(&grids[g]) as i64;
        check = (check * 31 + cost + r) % 1000000007;
    }
    println!("600 rounds over 20 grids of 100 by 100: checksum {}", check);
}
