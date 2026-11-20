// LeetCode #1730: Shortest Path to Get Food -- the bench (food.kara): a
// breadth-first search from you, the first food off the queue the
// nearest.

use std::collections::VecDeque;

fn get_food(grid: &[Vec<u8>]) -> i32 {
    let rows = grid.len() as i64;
    let cols = grid[0].len() as i64;
    let mut distance = vec![vec![-1i32; cols as usize]; rows as usize];
    let mut queue: VecDeque<(i64, i64)> = VecDeque::new();
    for r in 0..rows {
        for c in 0..cols {
            if grid[r as usize][c as usize] == b'*' {
                distance[r as usize][c as usize] = 0;
                queue.push_back((r, c));
            }
        }
    }
    while let Some((r, c)) = queue.pop_front() {
        if grid[r as usize][c as usize] == b'#' {
            return distance[r as usize][c as usize];
        }
        for (dr, dc) in [(-1i64, 0i64), (1, 0), (0, -1), (0, 1)] {
            let (nr, nc) = (r + dr, c + dc);
            if nr < 0 || nr >= rows || nc < 0 || nc >= cols {
                continue;
            }
            if grid[nr as usize][nc as usize] != b'X' && distance[nr as usize][nc as usize] < 0 {
                distance[nr as usize][nc as usize] = distance[r as usize][c as usize] + 1;
                queue.push_back((nr, nc));
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
    let count = 10;
    let rounds: i64 = 200;
    let side: i64 = 200;
    let mut seed: i64 = 1730;
    let mut problems: Vec<Vec<Vec<u8>>> = Vec::new();
    for _ in 0..count {
        let mut grid: Vec<Vec<u8>> = Vec::new();
        for _ in 0..side {
            let row: Vec<u8> = (0..side)
                .map(|_| {
                    let r = next_random(&mut seed) % 20000;
                    if r < 5000 {
                        b'X'
                    } else if r < 5001 {
                        b'#'
                    } else {
                        b'O'
                    }
                })
                .collect();
            grid.push(row);
        }
        let at = next_random(&mut seed) % (side * side);
        grid[(at / side) as usize][(at % side) as usize] = b'*';
        problems.push(grid);
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for grid in problems.iter() {
            let answer = get_food(grid) as i64;
            sum += answer;
            check = (check * 31 + answer + 1 + r) % 1000000007;
        }
    }
    println!(
        "{} grids of {} by {}, {} rounds: answers sum to {}, checksum {}",
        count, side, side, rounds, sum, check
    );
}
