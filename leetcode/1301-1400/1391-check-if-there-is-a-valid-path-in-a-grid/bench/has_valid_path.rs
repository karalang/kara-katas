// LeetCode #1391 bench, Rust mirror of the ★ arm.
use std::collections::VecDeque;

fn street_ways() -> Vec<Vec<(i64, i64)>> {
    vec![
        vec![],
        vec![(0, -1), (0, 1)],
        vec![(-1, 0), (1, 0)],
        vec![(0, -1), (1, 0)],
        vec![(0, 1), (1, 0)],
        vec![(0, -1), (-1, 0)],
        vec![(0, 1), (-1, 0)],
    ]
}

fn has_valid_path(grid: &[Vec<i32>]) -> bool {
    let m = grid.len() as i64;
    let n = grid[0].len() as i64;
    let ways = street_ways();
    let mut seen = vec![false; (m * n) as usize];
    let mut queue: VecDeque<(i64, i64)> = VecDeque::new();
    queue.push_back((0, 0));
    seen[0] = true;
    while let Some((r, c)) = queue.pop_front() {
        if r == m - 1 && c == n - 1 {
            return true;
        }
        for &(dr, dc) in ways[grid[r as usize][c as usize] as usize].iter() {
            let (nr, nc) = (r + dr, c + dc);
            if nr < 0 || nr >= m || nc < 0 || nc >= n || seen[(nr * n + nc) as usize] {
                continue;
            }
            if ways[grid[nr as usize][nc as usize] as usize].contains(&(-dr, -dc)) {
                seen[(nr * n + nc) as usize] = true;
                queue.push_back((nr, nc));
            }
        }
    }
    false
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let m: i64 = 299;
    let n: i64 = 300;
    let mut grid: Vec<Vec<i32>> = vec![vec![1; n as usize]; m as usize];
    for r in 0..(m - 1) as usize {
        let last = (n - 1) as usize;
        if r % 2 == 0 {
            grid[r][last] = 3;
            grid[r + 1][last] = 5;
        } else {
            grid[r][0] = 4;
            grid[r + 1][0] = 6;
        }
    }
    let mut seed: i64 = 1391;
    let mut check: i64 = 0;
    let whole = has_valid_path(&grid);
    for _ in 0..3000 {
        seed = (seed + check) % 2147483648;
        let cell = next_random(&mut seed) % (m * n);
        let (r, c) = ((cell / n) as usize, (cell % n) as usize);
        let street = grid[r][c];
        grid[r][c] = street % 6 + 1;
        let got = has_valid_path(&grid);
        grid[r][c] = street;
        check = (check * 131 + (if got { 2 } else { 1 }) * (cell + 1)) % 1000000007;
    }
    println!("3000 rounds over a 299 by 300 snake, whole {}: checksum {}", whole, check);
}
