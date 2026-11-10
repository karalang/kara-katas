// Benchmark: LeetCode #1091 Shortest Path in Binary Matrix -- Rust mirror of
// the ★ arm: breadth-first search with a `VecDeque` and a grid of
// distances. Same workload and sink as shortest_path_binary_matrix.kara.

use std::collections::VecDeque;

fn shortest_path_binary_matrix(grid: &[Vec<i64>]) -> i64 {
    let n = grid.len() as i64;
    if grid[0][0] == 1 || grid[(n - 1) as usize][(n - 1) as usize] == 1 {
        return -1;
    }
    let mut dist = vec![vec![-1i64; n as usize]; n as usize];
    dist[0][0] = 1;
    let mut queue: VecDeque<(i64, i64)> = VecDeque::new();
    queue.push_back((0, 0));
    while let Some((r, c)) = queue.pop_front() {
        if r == n - 1 && c == n - 1 {
            return dist[r as usize][c as usize];
        }
        for dr in -1..=1 {
            for dc in -1..=1 {
                let (nr, nc) = (r + dr, c + dc);
                if nr >= 0
                    && nr < n
                    && nc >= 0
                    && nc < n
                    && grid[nr as usize][nc as usize] == 0
                    && dist[nr as usize][nc as usize] == -1
                {
                    dist[nr as usize][nc as usize] = dist[r as usize][c as usize] + 1;
                    queue.push_back((nr, nc));
                }
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
    let mut seed = 1091;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for k in 0..200 {
        let blocked = 25 + k % 20;
        let mut grid: Vec<Vec<i64>> = Vec::new();
        for _ in 0..100 {
            let mut row = Vec::new();
            for _ in 0..100 {
                row.push(if next_random(&mut seed) % 100 < blocked { 1 } else { 0 });
            }
            grid.push(row);
        }
        grid[0][0] = 0;
        grid[99][99] = 0;
        grids.push(grid);
    }
    let (mut none, mut total, mut check) = (0i64, 0i64, 0i64);
    for _ in 0..20 {
        for grid in grids.iter() {
            let answer = shortest_path_binary_matrix(grid);
            if answer == -1 {
                none += 1;
            } else {
                total += answer;
            }
            check = (check * 31 + answer + 1) % 1000000007;
        }
    }
    println!("20 rounds over 200 grids of 100 by 100: {} without a path, lengths sum to {}, checksum {}", none, total, check);
}
