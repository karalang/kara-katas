// LeetCode #1263 bench, in Rust: the ★ arm's 0-1 BFS over (box, player)
// states (a step to the front of a `VecDeque`, a push to the back, a state
// final the first time it leaves) on 100 random 20 by 20 grids, a cell in
// 10 a wall, built once, 20 rounds; every answer folded into a checksum.
use std::collections::VecDeque;

fn min_push_box(grid: &[Vec<u8>]) -> i64 {
    let m = grid.len() as i64;
    let n = grid[0].len() as i64;
    let (mut player, mut box_at, mut target) = (0i64, 0i64, 0i64);
    for r in 0..m {
        for c in 0..n {
            match grid[r as usize][c as usize] {
                b'S' => player = r * n + c,
                b'B' => box_at = r * n + c,
                b'T' => target = r * n + c,
                _ => {}
            }
        }
    }
    let cells = m * n;
    let mut done = vec![false; (cells * cells) as usize];
    let mut deque: VecDeque<(i64, i64, i64)> = VecDeque::new();
    deque.push_back((box_at, player, 0));
    while let Some((b, p, pushes)) = deque.pop_front() {
        if done[(b * cells + p) as usize] {
            continue;
        }
        done[(b * cells + p) as usize] = true;
        if b == target {
            return pushes;
        }
        for (dr, dc) in [(-1i64, 0i64), (1, 0), (0, -1), (0, 1)] {
            let r = p / n + dr;
            let c = p % n + dc;
            if r < 0 || r >= m || c < 0 || c >= n || grid[r as usize][c as usize] == b'#' {
                continue;
            }
            let q = r * n + c;
            if q != b {
                deque.push_front((b, q, pushes));
                continue;
            }
            let br = r + dr;
            let bc = c + dc;
            if br >= 0 && br < m && bc >= 0 && bc < n && grid[br as usize][bc as usize] != b'#' {
                deque.push_back((br * n + bc, q, pushes + 1));
            }
        }
    }
    -1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_grid(m: i64, n: i64, walls: i64, seed: &mut i64) -> Vec<Vec<u8>> {
    let mut grid: Vec<Vec<u8>> = (0..m)
        .map(|_| (0..n).map(|_| if next_random(seed) % walls == 0 { b'#' } else { b'.' }).collect())
        .collect();
    for mark in [b'S', b'B', b'T'] {
        let mut p = next_random(seed) % (m * n);
        while matches!(grid[(p / n) as usize][(p % n) as usize], b'S' | b'B' | b'T') {
            p = (p + 1) % (m * n);
        }
        grid[(p / n) as usize][(p % n) as usize] = mark;
    }
    grid
}

fn main() {
    let mut seed = 1263i64;
    let grids: Vec<Vec<Vec<u8>>> = (0..100).map(|_| random_grid(20, 20, 10, &mut seed)).collect();
    let mut check = 0i64;
    let mut total = 0i64;
    for round in 0..20 {
        for g in &grids {
            let pushes = min_push_box(g);
            if pushes > 0 {
                total += pushes;
            }
            check = (check * 131 + pushes + 1 + round) % 1000000007;
        }
    }
    println!("20 rounds of 100 grids of 20 by 20: {} pushes, checksum {}", total, check);
}
